from pydantic import BaseModel
from typing import List


class VendorScore(BaseModel):
    vendor_name: str

    technical_score: float
    geographic_score: float
    quantity_score: float
    evidence_score: float
    delivery_score: float

    total_score: float

    ranking_reason: List[str]
    risks: List[str]