from typing import Optional
from pydantic import BaseModel


class VendorCandidate(BaseModel):
    vendor_name: str

    location: Optional[str] = None
    country: Optional[str] = None

    vendor_type: Optional[str] = None

    website: Optional[str] = None

    product_evidence: list[str] = []
    source_urls: list[str] = []

    geographic_category: str

    confidence: str