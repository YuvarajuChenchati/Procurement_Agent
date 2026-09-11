from typing import Literal, Optional

from pydantic import BaseModel

from app.schemas.source import Source


class EvidenceItem(BaseModel):

    criterion: str

    status: Literal[
        "confirmed",
        "partial",
        "not_found",
        "conflicting"
    ]

    evidence: str

    source_url: Optional[str] = None


class VendorEvidence(BaseModel):

    vendor_name: str

    sources: list[Source]

    product_evidence: list[EvidenceItem]

    specification_evidence: list[EvidenceItem]

    standard_evidence: list[EvidenceItem]

    geography_evidence: list[EvidenceItem]

    quantity_evidence: list[EvidenceItem]

    delivery_evidence: list[EvidenceItem]

    unresolved_issues: list[str]
