import csv
import io
import json
import time

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import Response

from app.schemas.input import ProcurementRequest
from app.graph.workflow import graph
from app.services.logger import (
    log_api_end,
    log_api_error,
    log_api_start,
    log_info,
)


app = FastAPI(
    title="Agentic Procurement Tool",
    description="AI-powered industrial vendor discovery and evaluation",
    version="1.0.0"
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health")
def health_check():
    return {
        "status": "ok",
        "service": "agentic-procurement-tool"
    }


@app.post("/procurement/analyze")
def analyze_procurement(
    request: ProcurementRequest
):
    t_start = time.time()
    req_dict = request.model_dump()
    loc = req_dict.get("location") or {}
    loc_str = f"{loc.get('city', 'N/A')}, {loc.get('country', 'N/A')}"
    days = req_dict.get("delivery_timeline_days")
    timeline_str = f"{days} days" if days is not None else "Not specified"

    log_api_start(
        "/procurement/analyze",
        {
            "Requirement": req_dict.get("raw_requirement", "N/A"),
            "Target Location": loc_str,
            "Quantity": req_dict.get("quantity") or "Not specified",
            "Delivery Timeline": timeline_str,
        }
    )

    try:
        initial_state = {
            "request": req_dict
        }

        result = graph.invoke(initial_state)
        report = result.get("final_report", {})

        ahm_count = len(report.get("ahmedabad_vendors", []))
        ind_count = len(report.get("india_vendors", []))
        glo_count = len(report.get("global_vendors", []))
        exc_count = len(report.get("excluded_or_unverified", []))
        total_shortlisted = ahm_count + ind_count + glo_count

        log_api_end(
            "/procurement/analyze",
            time.time() - t_start,
            {
                "Total Shortlisted": total_shortlisted,
                "Ahmedabad Vendors": ahm_count,
                "India Vendors": ind_count,
                "Global Vendors": glo_count,
                "Excluded / Unverified": exc_count,
            }
        )

        return {
            "success": True,
            "report": report
        }

    except Exception as e:
        duration = time.time() - t_start
        log_api_error("/procurement/analyze", duration, str(e))
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )


@app.post("/procurement/export/{format_name}")
def export_procurement(request: ProcurementRequest, format_name: str):
    """Run the same evidence-backed analysis and return a portable report."""
    t_start = time.time()
    log_api_start(
        f"/procurement/export/{format_name}",
        {
            "Format": format_name,
            "Requirement": request.raw_requirement,
        }
    )

    try:
        report = graph.invoke({"request": request.model_dump()}).get("final_report", {})
        if format_name == "json":
            content = json.dumps(report, indent=2)
            log_api_end(f"/procurement/export/{format_name}", time.time() - t_start, {"Size (bytes)": len(content)})
            return Response(content, media_type="application/json", headers={"Content-Disposition": "attachment; filename=procurement-report.json"})
        if format_name == "csv":
            rows = [vendor for group in ("ahmedabad_vendors", "india_vendors", "global_vendors", "excluded_or_unverified") for vendor in report.get(group, [])]
            output = io.StringIO()
            writer = csv.DictWriter(output, fieldnames=["vendor_name", "location", "country", "vendor_type", "website", "match_type", "confidence", "total_score", "recommended_next_step", "source_urls"])
            writer.writeheader()
            for vendor in rows:
                writer.writerow({key: "; ".join(value) if isinstance(value := vendor.get(key), list) else value for key in writer.fieldnames})
            content = output.getvalue()
            log_api_end(f"/procurement/export/{format_name}", time.time() - t_start, {"Rows Exported": len(rows), "Size (bytes)": len(content)})
            return Response(content, media_type="text/csv", headers={"Content-Disposition": "attachment; filename=procurement-report.csv"})
        raise HTTPException(status_code=400, detail="Supported formats are json and csv.")
    except HTTPException as exc:
        log_api_error(f"/procurement/export/{format_name}", time.time() - t_start, exc.detail)
        raise
    except Exception as exc:
        log_api_error(f"/procurement/export/{format_name}", time.time() - t_start, str(exc))
        raise HTTPException(status_code=500, detail=str(exc))
