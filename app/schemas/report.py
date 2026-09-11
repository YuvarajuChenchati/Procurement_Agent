from typing import Literal, Optional
from pydantic import BaseModel

from app.schemas.output import Ambiguity
from app.schemas.input import ProcurementRequest


class VendorReport(BaseModel):

    vendor_name: str
    location: str | None = None
    country: str | None = None
    vendor_type: str | None = None
    website: Optional[str] = None
    contact_details: list[str] = []

    geographic_category: Literal[
        "ahmedabad",
        "india",
        "global",
        "unknown"
    ]

    match_type: Literal[
        "exact_match",
        "near_match",
        "category_lead",
        "unverified"
    ]

    recommendation_status: Literal[
        "shortlist_candidate",
        "needs_verification",
        "unverified"
    ]

    confidence: Literal[
        "high",
        "medium",
        "low"
    ]

    total_score: float

    key_evidence: list[str]

    unresolved_issues: list[str]

    recommended_next_step: str

    source_urls: list[str]


class ProcurementReport(BaseModel):

    request_id: str

    original_requirement: ProcurementRequest

    assumptions: list[str]

    ambiguities: list[Ambiguity]

    search_issues: list[str] = []

    ahmedabad_vendors: list[VendorReport]

    india_vendors: list[VendorReport]

    global_vendors: list[VendorReport]

    excluded_or_unverified: list[VendorReport]
