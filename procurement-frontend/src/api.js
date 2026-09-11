const API_BASE_URL = "http://localhost:8000";


export async function analyzeProcurement(request) {

    const response = await fetch(
        `${API_BASE_URL}/procurement/analyze`,
        {
            method: "POST",

            headers: {
                "Content-Type": "application/json"
            },

            body: JSON.stringify(request)
        }
    );


    if (!response.ok) {

        const error = await response.json();

        throw new Error(
            error.detail || "Procurement analysis failed"
        );
    }


    return response.json();
}

export function downloadReport(report, format) {
    const vendors = [...(report.ahmedabad_vendors || []), ...(report.india_vendors || []), ...(report.global_vendors || []), ...(report.excluded_or_unverified || [])];
    const content = format === "json" ? JSON.stringify(report, null, 2) : [
        "vendor_name,location,country,match_type,confidence,total_score,website",
        ...vendors.map((vendor) => ["vendor_name", "location", "country", "match_type", "confidence", "total_score", "website"].map((key) => `"${String(vendor[key] || "").replaceAll('"', '""')}"`).join(",")),
    ].join("\n");
    const blob = new Blob([content], { type: format === "json" ? "application/json" : "text/csv" });
    const url = URL.createObjectURL(blob);
    const anchor = document.createElement("a");
    anchor.href = url;
    anchor.download = `procurement-report.${format}`;
    anchor.click();
    URL.revokeObjectURL(url);
}
