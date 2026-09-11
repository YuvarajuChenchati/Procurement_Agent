from typing import List, Literal, Optional
from pydantic import BaseModel


class EvidenceCheck(BaseModel):
    criterion: str
    status: Literal[
        "confirmed",
        "partial",
        "not_found",
        "conflicting"
    ]
    evidence: str
    source_url: Optional[str] = None


class VendorVerification(BaseModel):
    vendor_name: str

    match_type: Literal[
        "exact_match",
        "near_match",
        "category_lead",
        "unverified"
    ]

    technical_match: str
    geographic_match: str
    quantity_feasibility: str

    evidence_checks: List[EvidenceCheck]

    unresolved_issues: List[str]
    recommended_next_step: str

    confidence: Literal[
        "high",
        "medium",
        "low"
    ]