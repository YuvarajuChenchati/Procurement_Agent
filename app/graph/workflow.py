"""The explicit, fault-tolerant procurement research workflow."""

from concurrent.futures import ThreadPoolExecutor, as_completed

from langgraph.graph import END, START, StateGraph

from app.agents.evidence_verifier import verify_vendor
from app.agents.procurement_evaluator import evaluate_vendor
from app.agents.report_generator import generate_report
from app.agents.requirement_analyzer import analyze_requirement
from app.agents.research_agent import generate_search_queries
from app.agents.source_researcher import research_vendor
from app.agents.vendor_extractor import extract_vendors
from app.graph.state import ProcurementState
from app.services.geography import classify_geography
from app.services.candidate_selector import select_candidates
from app.services.ranking import calculate_vendor_score
from app.services.vendor_normalizer import deduplicate_vendors
from app.tools.web_search import web_search


# The assessment is a live-research demo, so keep its request fan-out small and
# run independent network calls concurrently.  This avoids a long serial chain
# while still retaining a geographically balanced shortlist.
SEARCHES_PER_CATEGORY = 2
CANDIDATES_PER_CATEGORY = 2
MAX_PARALLEL_REQUESTS = 3


def _parallel_map(items, operation):
    """Run independent remote operations concurrently and preserve input order."""
    results = [None] * len(items)
    with ThreadPoolExecutor(max_workers=min(MAX_PARALLEL_REQUESTS, len(items) or 1)) as executor:
        futures = {executor.submit(operation, item): index for index, item in enumerate(items)}
        for future in as_completed(futures):
            results[futures[future]] = future.result()
    return results


def analyze_node(state: ProcurementState):
    return {"analysis": analyze_requirement(state["request"]).model_dump()}


def research_node(state: ProcurementState):
    return {"search_queries": generate_search_queries(state["analysis"]["normalized_requirement"])}


def search_node(state: ProcurementState):
    jobs = []
    for category, queries in state["search_queries"].items():
        for query in queries[:SEARCHES_PER_CATEGORY]:
            jobs.append((category, query))

    def search(job):
        category, query = job
        try:
            return {"category": category, "query": query, "status": "success", **web_search(query)}
        except Exception as exc:
            return {"category": category, "query": query, "text": "", "sources": [], "status": "failed", "error": str(exc)}

    return {"search_results": _parallel_map(jobs, search)}


def vendor_extraction_node(state: ProcurementState):
    grouped_results = {}
    for result in state["search_results"]:
        if result["text"]:
            grouped_results.setdefault(result["category"], []).append(result)

    def extract(item):
        category, results = item
        try:
            return extract_vendors(results, category)
        except Exception as exc:
            for result in results:
                result["extraction_error"] = str(exc)
            return []

    extracted = _parallel_map(list(grouped_results.items()), extract)
    return {"vendors": [vendor for group in extracted for vendor in group]}


def deduplicate_node(state: ProcurementState):
    return {"vendors": deduplicate_vendors(state["vendors"])}


def geography_node(state: ProcurementState):
    location = state["request"]["location"]
    classified = []
    for vendor in state["vendors"]:
        copy = vendor.copy()
        copy["geographic_category"] = classify_geography(vendor.get("location"), vendor.get("country"), location["city"], location["country"])
        classified.append(copy)
    return {"vendors": classified}


def candidate_selection_node(state: ProcurementState):
    """Bound live source research to two vendors per geographic category."""
    return {"vendors": select_candidates(state["vendors"], limit_per_category=CANDIDATES_PER_CATEGORY)}


def source_research_node(state: ProcurementState):
    def research(vendor):
        try:
            return research_vendor(state["analysis"], vendor).model_dump()
        except Exception as exc:
            return {"vendor_name": vendor["vendor_name"], "sources": [], "product_evidence": [], "specification_evidence": [], "standard_evidence": [], "geography_evidence": [], "quantity_evidence": [], "delivery_evidence": [], "unresolved_issues": [f"Source research failed: {exc}"]}

    return {"evidence": _parallel_map(state["vendors"], research)}


def verification_node(state: ProcurementState):
    by_name = {vendor["vendor_name"]: vendor for vendor in state["vendors"]}
    def verify(evidence):
        vendor = by_name.get(evidence["vendor_name"])
        if not vendor:
            return None
        try:
            return verify_vendor(state["analysis"], vendor, evidence).model_dump()
        except Exception as exc:
            return {"vendor_name": vendor["vendor_name"], "match_type": "unverified", "technical_match": "Verification failed", "geographic_match": "Unknown", "quantity_feasibility": "Unknown", "evidence_checks": [], "unresolved_issues": [f"Verification failed: {exc}"], "recommended_next_step": "Verify directly with the vendor.", "confidence": "low"}

    return {"verifications": [item for item in _parallel_map(state["evidence"], verify) if item]}


def evaluation_node(state: ProcurementState):
    def evaluate(verification):
        try:
            return evaluate_vendor(state["analysis"], verification).model_dump()
        except Exception as exc:
            return {"vendor_name": verification["vendor_name"], "technical_score": 0, "geographic_score": 0, "quantity_score": 0, "evidence_score": 0, "delivery_score": 0, "score_reasoning": [f"Evaluation failed: {exc}"], "risks": verification["unresolved_issues"], "recommended_next_step": verification["recommended_next_step"]}

    return {"evaluations": _parallel_map(state["verifications"], evaluate)}


def ranking_node(state: ProcurementState):
    rankings = []
    for item in state["evaluations"]:
        score = calculate_vendor_score(item["technical_score"], item["geographic_score"], item["quantity_score"], item["evidence_score"], item["delivery_score"])
        rankings.append({**item, "total_score": score})
    return {"rankings": sorted(rankings, key=lambda item: item["total_score"], reverse=True)}


def report_node(state: ProcurementState):
    report = generate_report(state["request"], state["analysis"], state["vendors"], state["verifications"], state["rankings"], state.get("search_results", []))
    return {"final_report": report.model_dump()}


builder = StateGraph(ProcurementState)
for name, function in (("analyze_requirement", analyze_node), ("generate_queries", research_node), ("search_web", search_node), ("extract_vendors", vendor_extraction_node), ("deduplicate_vendors", deduplicate_node), ("classify_geography", geography_node), ("select_candidates", candidate_selection_node), ("research_vendor_sources", source_research_node), ("verify_evidence", verification_node), ("evaluate_vendors", evaluation_node), ("rank_vendors", ranking_node), ("generate_report", report_node)):
    builder.add_node(name, function)
for source, target in ((START, "analyze_requirement"), ("analyze_requirement", "generate_queries"), ("generate_queries", "search_web"), ("search_web", "extract_vendors"), ("extract_vendors", "deduplicate_vendors"), ("deduplicate_vendors", "classify_geography"), ("classify_geography", "select_candidates"), ("select_candidates", "research_vendor_sources"), ("research_vendor_sources", "verify_evidence"), ("verify_evidence", "evaluate_vendors"), ("evaluate_vendors", "rank_vendors"), ("rank_vendors", "generate_report"), ("generate_report", END)):
    builder.add_edge(source, target)

graph = builder.compile()
