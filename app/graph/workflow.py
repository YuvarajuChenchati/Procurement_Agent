"""The explicit, fault-tolerant procurement research workflow."""

import time
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
from app.services.candidate_selector import select_candidates
from app.services.geography import classify_geography
from app.services.logger import (
    log_step_end,
    log_step_start,
    log_substep,
)
from app.services.ranking import calculate_vendor_score
from app.services.vendor_normalizer import deduplicate_vendors
from app.tools.web_search import web_search

TOTAL_STEPS = 12

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
    t0 = time.time()
    raw_req = state.get("request", {}).get("raw_requirement", "")
    log_step_start(1, TOTAL_STEPS, "Analyze Requirement", f"Input: {raw_req[:60]}...")

    analysis = analyze_requirement(state["request"]).model_dump()

    norm = analysis.get("normalized_requirement", {})
    material = norm.get("material", "N/A")
    spec = norm.get("specification", "N/A")
    qty_obj = norm.get("quantity", {}) or {}
    qty_str = f"{qty_obj.get('value', 'N/A')} {qty_obj.get('unit', '')}".strip()
    ambiguities = analysis.get("technical_ambiguities", [])

    log_substep(f"Extracted Material: {material}")
    log_substep(f"Specification: {spec} | Quantity: {qty_str}")
    if ambiguities:
        log_substep(f"Ambiguities flagged ({len(ambiguities)}): {'; '.join(ambiguities[:3])}")

    log_step_end(1, TOTAL_STEPS, "Analyze Requirement", time.time() - t0, f"Material: {material}")
    return {"analysis": analysis}


def research_node(state: ProcurementState):
    t0 = time.time()
    log_step_start(2, TOTAL_STEPS, "Generate Search Queries", "Planning search queries across geography tiers")

    queries = generate_search_queries(state["analysis"]["normalized_requirement"])

    ahm_cnt = len(queries.get("ahmedabad", []))
    ind_cnt = len(queries.get("india", []))
    glo_cnt = len(queries.get("global", []))

    log_substep(f"Search queries planned: Ahmedabad ({ahm_cnt}), India ({ind_cnt}), Global ({glo_cnt})")
    for category in ("ahmedabad", "india", "global"):
        sample_queries = queries.get(category, [])
        for idx, q in enumerate(sample_queries[:SEARCHES_PER_CATEGORY], 1):
            log_substep(f"[{category.capitalize()} Q{idx}] \"{q}\"")

    log_step_end(2, TOTAL_STEPS, "Generate Search Queries", time.time() - t0, f"Total planned: {ahm_cnt + ind_cnt + glo_cnt} queries")
    return {"search_queries": queries}


def search_node(state: ProcurementState):
    t0 = time.time()
    jobs = []
    for category, queries in state["search_queries"].items():
        for query in queries[:SEARCHES_PER_CATEGORY]:
            jobs.append((category, query))

    total_jobs = len(jobs)
    log_step_start(3, TOTAL_STEPS, "Web Search", f"Executing {total_jobs} queries with web search tool")

    def search(job):
        category, query = job
        log_substep(f"Starting search [{category.upper()}]: \"{query}\"")
        try:
            res = web_search(query)
            source_count = len(res.get("sources", []))
            log_substep(f"[OK] Search [{category.upper()}]: \"{query[:45]}...\" -> {source_count} sources found")
            return {"category": category, "query": query, "status": "success", **res}
        except Exception as exc:
            log_substep(f"[FAILED] Search [{category.upper()}]: \"{query[:45]}...\" -> Error: {exc}")
            return {"category": category, "query": query, "text": "", "sources": [], "status": "failed", "error": str(exc)}

    search_results = _parallel_map(jobs, search)
    successful = sum(1 for r in search_results if r.get("status") == "success")
    total_sources = sum(len(r.get("sources", [])) for r in search_results)

    log_step_end(3, TOTAL_STEPS, "Web Search", time.time() - t0, f"{successful}/{total_jobs} queries succeeded, {total_sources} total sources collected")
    return {"search_results": search_results}


def vendor_extraction_node(state: ProcurementState):
    t0 = time.time()
    grouped_results = {}
    for result in state["search_results"]:
        if result["text"]:
            grouped_results.setdefault(result["category"], []).append(result)

    log_step_start(4, TOTAL_STEPS, "Extract Vendors", f"Parsing vendor entities from {len(grouped_results)} geographic result sets")

    def extract(item):
        category, results = item
        log_substep(f"Extracting vendors from [{category.upper()}] search texts ({len(results)} queries)...")
        try:
            vendors = extract_vendors(results, category)
            log_substep(f"[OK] Extracted {len(vendors)} vendors for [{category.upper()}]")
            return vendors
        except Exception as exc:
            log_substep(f"[FAILED] Extraction failed for [{category.upper()}]: {exc}")
            for result in results:
                result["extraction_error"] = str(exc)
            return []

    extracted = _parallel_map(list(grouped_results.items()), extract)
    all_vendors = [vendor for group in extracted for vendor in group]

    log_step_end(4, TOTAL_STEPS, "Extract Vendors", time.time() - t0, f"Found {len(all_vendors)} raw vendor candidates")
    return {"vendors": all_vendors}


def deduplicate_node(state: ProcurementState):
    t0 = time.time()
    before_count = len(state["vendors"])
    log_step_start(5, TOTAL_STEPS, "Deduplicate Vendors", f"Input: {before_count} candidates")

    deduped = deduplicate_vendors(state["vendors"])
    after_count = len(deduped)

    log_substep(f"Deduplication: {before_count} candidates -> {after_count} unique vendors (removed {before_count - after_count} duplicates)")
    log_step_end(5, TOTAL_STEPS, "Deduplicate Vendors", time.time() - t0, f"{after_count} unique vendors remaining")
    return {"vendors": deduped}


def geography_node(state: ProcurementState):
    t0 = time.time()
    location = state["request"]["location"]
    city = location.get("city", "")
    country = location.get("country", "")

    log_step_start(6, TOTAL_STEPS, "Classify Geography", f"Target benchmark: {city}, {country}")

    classified = []
    for vendor in state["vendors"]:
        copy = vendor.copy()
        copy["geographic_category"] = classify_geography(vendor.get("location"), vendor.get("country"), city, country)
        classified.append(copy)

    ahm_cnt = sum(1 for v in classified if v.get("geographic_category") == "ahmedabad")
    ind_cnt = sum(1 for v in classified if v.get("geographic_category") == "india")
    glo_cnt = sum(1 for v in classified if v.get("geographic_category") == "global")
    oth_cnt = len(classified) - (ahm_cnt + ind_cnt + glo_cnt)

    log_substep(f"Geography breakdown: Ahmedabad={ahm_cnt}, India={ind_cnt}, Global={glo_cnt}, Other={oth_cnt}")
    log_step_end(6, TOTAL_STEPS, "Classify Geography", time.time() - t0, f"{len(classified)} vendors classified")
    return {"vendors": classified}


def candidate_selection_node(state: ProcurementState):
    t0 = time.time()
    log_step_start(7, TOTAL_STEPS, "Select Candidates", f"Filtering to top {CANDIDATES_PER_CATEGORY} vendors per geographic tier")

    selected = select_candidates(state["vendors"], limit_per_category=CANDIDATES_PER_CATEGORY)
    for v in selected:
        log_substep(f"Candidate: {v.get('vendor_name')} | Tier: {v.get('geographic_category')} | Loc: {v.get('location', 'N/A')}")

    log_step_end(7, TOTAL_STEPS, "Select Candidates", time.time() - t0, f"{len(selected)} candidate vendors shortlisted for deep research")
    return {"vendors": selected}


def source_research_node(state: ProcurementState):
    t0 = time.time()
    total = len(state["vendors"])
    log_step_start(8, TOTAL_STEPS, "Research Vendor Sources", f"Performing deep investigation on {total} candidate vendors in parallel")

    def research(vendor):
        vname = vendor.get("vendor_name", "Unknown")
        log_substep(f"Investigating vendor: {vname}...")
        try:
            res = research_vendor(state["analysis"], vendor).model_dump()
            sources_count = len(res.get("sources", []))
            ev_count = len(res.get("product_evidence", []))
            log_substep(f"[OK] Research completed for {vname} ({sources_count} sources, {ev_count} product evidence)")
            return res
        except Exception as exc:
            log_substep(f"[FAILED] Research failed for {vname}: {exc}")
            return {
                "vendor_name": vname,
                "sources": [],
                "product_evidence": [],
                "specification_evidence": [],
                "standard_evidence": [],
                "geography_evidence": [],
                "quantity_evidence": [],
                "delivery_evidence": [],
                "unresolved_issues": [f"Source research failed: {exc}"]
            }

    evidence = _parallel_map(state["vendors"], research)
    log_step_end(8, TOTAL_STEPS, "Research Vendor Sources", time.time() - t0, f"Evidence gathered for {len(evidence)} vendors")
    return {"evidence": evidence}


def verification_node(state: ProcurementState):
    t0 = time.time()
    total = len(state["evidence"])
    log_step_start(9, TOTAL_STEPS, "Verify Evidence", f"Validating specs, compliance, and claims for {total} vendors")

    by_name = {vendor["vendor_name"]: vendor for vendor in state["vendors"]}

    def verify(evidence):
        vendor = by_name.get(evidence["vendor_name"])
        if not vendor:
            return None
        vname = vendor.get("vendor_name", "Unknown")
        log_substep(f"Verifying claims for {vname}...")
        try:
            ver = verify_vendor(state["analysis"], vendor, evidence).model_dump()
            log_substep(f"[OK] Verified {vname} -> Match: {ver.get('match_type')}, Confidence: {ver.get('confidence')}")
            return ver
        except Exception as exc:
            log_substep(f"[FAILED] Verification failed for {vname}: {exc}")
            return {
                "vendor_name": vname,
                "match_type": "unverified",
                "technical_match": "Verification failed",
                "geographic_match": "Unknown",
                "quantity_feasibility": "Unknown",
                "evidence_checks": [],
                "unresolved_issues": [f"Verification failed: {exc}"],
                "recommended_next_step": "Verify directly with the vendor.",
                "confidence": "low"
            }

    verifications = [item for item in _parallel_map(state["evidence"], verify) if item]
    log_step_end(9, TOTAL_STEPS, "Verify Evidence", time.time() - t0, f"Verified {len(verifications)} vendors")
    return {"verifications": verifications}


def evaluation_node(state: ProcurementState):
    t0 = time.time()
    total = len(state["verifications"])
    log_step_start(10, TOTAL_STEPS, "Evaluate Vendors", f"Scoring technical match, geography, quantity, and delivery for {total} vendors")

    def evaluate(verification):
        vname = verification.get("vendor_name", "Unknown")
        log_substep(f"Evaluating scorecard for {vname}...")
        try:
            ev = evaluate_vendor(state["analysis"], verification).model_dump()
            log_substep(f"[OK] Evaluated {vname} -> Tech: {ev.get('technical_score')}, Geo: {ev.get('geographic_score')}, Qty: {ev.get('quantity_score')}, Delivery: {ev.get('delivery_score')}")
            return ev
        except Exception as exc:
            log_substep(f"[FAILED] Evaluation failed for {vname}: {exc}")
            return {
                "vendor_name": vname,
                "technical_score": 0,
                "geographic_score": 0,
                "quantity_score": 0,
                "evidence_score": 0,
                "delivery_score": 0,
                "score_reasoning": [f"Evaluation failed: {exc}"],
                "risks": verification.get("unresolved_issues", []),
                "recommended_next_step": verification.get("recommended_next_step", "Verify directly.")
            }

    evaluations = _parallel_map(state["verifications"], evaluate)
    log_step_end(10, TOTAL_STEPS, "Evaluate Vendors", time.time() - t0, f"Evaluated {len(evaluations)} vendors")
    return {"evaluations": evaluations}


def ranking_node(state: ProcurementState):
    t0 = time.time()
    log_step_start(11, TOTAL_STEPS, "Rank Vendors", "Calculating composite weighted score for all evaluated vendors")

    rankings = []
    for item in state["evaluations"]:
        score = calculate_vendor_score(
            item["technical_score"],
            item["geographic_score"],
            item["quantity_score"],
            item["evidence_score"],
            item["delivery_score"]
        )
        rankings.append({**item, "total_score": score})

    ranked = sorted(rankings, key=lambda item: item["total_score"], reverse=True)
    log_substep("Vendor Leaderboard:")
    for rank, v in enumerate(ranked, 1):
        log_substep(f"  #{rank}: {v['vendor_name']} -> Total Score: {v['total_score']:.1f}/100 (Tech: {v.get('technical_score')}, Geo: {v.get('geographic_score')}, Qty: {v.get('quantity_score')})")

    log_step_end(11, TOTAL_STEPS, "Rank Vendors", time.time() - t0, f"{len(ranked)} vendors ranked")
    return {"rankings": ranked}


def report_node(state: ProcurementState):
    t0 = time.time()
    log_step_start(12, TOTAL_STEPS, "Generate Report", "Assembling final evidence-backed procurement report")

    report = generate_report(
        state["request"],
        state["analysis"],
        state["vendors"],
        state["verifications"],
        state["rankings"],
        state.get("search_results", [])
    )
    rep_dict = report.model_dump()

    ahm_cnt = len(rep_dict.get("ahmedabad_vendors", []))
    ind_cnt = len(rep_dict.get("india_vendors", []))
    glo_cnt = len(rep_dict.get("global_vendors", []))
    exc_cnt = len(rep_dict.get("excluded_or_unverified", []))

    log_substep(f"Final report distribution: Ahmedabad: {ahm_cnt} | India: {ind_cnt} | Global: {glo_cnt} | Excluded/Unverified: {exc_cnt}")
    log_step_end(12, TOTAL_STEPS, "Generate Report", time.time() - t0, "Final report generated successfully")
    return {"final_report": rep_dict}


builder = StateGraph(ProcurementState)
for name, function in (
    ("analyze_requirement", analyze_node),
    ("generate_queries", research_node),
    ("search_web", search_node),
    ("extract_vendors", vendor_extraction_node),
    ("deduplicate_vendors", deduplicate_node),
    ("classify_geography", geography_node),
    ("select_candidates", candidate_selection_node),
    ("research_vendor_sources", source_research_node),
    ("verify_evidence", verification_node),
    ("evaluate_vendors", evaluation_node),
    ("rank_vendors", ranking_node),
    ("generate_report", report_node)
):
    builder.add_node(name, function)

for source, target in (
    (START, "analyze_requirement"),
    ("analyze_requirement", "generate_queries"),
    ("generate_queries", "search_web"),
    ("search_web", "extract_vendors"),
    ("extract_vendors", "deduplicate_vendors"),
    ("deduplicate_vendors", "classify_geography"),
    ("classify_geography", "select_candidates"),
    ("select_candidates", "research_vendor_sources"),
    ("research_vendor_sources", "verify_evidence"),
    ("verify_evidence", "evaluate_vendors"),
    ("evaluate_vendors", "rank_vendors"),
    ("rank_vendors", "generate_report"),
    ("generate_report", END)
):
    builder.add_edge(source, target)

graph = builder.compile()
