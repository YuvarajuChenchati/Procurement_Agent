import csv
import io
import json

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import Response

from app.schemas.input import ProcurementRequest
from app.graph.workflow import graph


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

    try:

        initial_state = {
            "request": request.model_dump()
        }

        result = graph.invoke(
            initial_state
        )

        return {
            "success": True,
            "report": result.get("final_report")
        }

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )


@app.post("/procurement/export/{format_name}")
def export_procurement(request: ProcurementRequest, format_name: str):
    """Run the same evidence-backed analysis and return a portable report."""
    try:
        report = graph.invoke({"request": request.model_dump()}).get("final_report")
        if format_name == "json":
            return Response(json.dumps(report, indent=2), media_type="application/json", headers={"Content-Disposition": "attachment; filename=procurement-report.json"})
        if format_name == "csv":
            rows = [vendor for group in ("ahmedabad_vendors", "india_vendors", "global_vendors", "excluded_or_unverified") for vendor in report.get(group, [])]
            output = io.StringIO()
            writer = csv.DictWriter(output, fieldnames=["vendor_name", "location", "country", "vendor_type", "website", "match_type", "confidence", "total_score", "recommended_next_step", "source_urls"])
            writer.writeheader()
            for vendor in rows:
                writer.writerow({key: "; ".join(value) if isinstance(value := vendor.get(key), list) else value for key in writer.fieldnames})
            return Response(output.getvalue(), media_type="text/csv", headers={"Content-Disposition": "attachment; filename=procurement-report.csv"})
        raise HTTPException(status_code=400, detail="Supported formats are json and csv.")
    except HTTPException:
        raise
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc))
