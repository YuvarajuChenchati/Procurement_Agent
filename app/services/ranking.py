def calculate_vendor_score(
    technical_match: float,
    geographic_match: float,
    quantity_feasibility: float,
    evidence_quality: float,
    delivery_capability: float,
):
    score = (
        technical_match * 0.35
        + geographic_match * 0.20
        + quantity_feasibility * 0.20
        + evidence_quality * 0.15
        + delivery_capability * 0.10
    )

    return round(score, 2)