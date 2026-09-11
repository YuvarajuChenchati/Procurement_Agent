from pydantic import BaseModel, Field


class ProcurementEvaluation(BaseModel):
    vendor_name: str

    technical_score: float = Field(
        ge=0,
        le=100
    )

    geographic_score: float = Field(
        ge=0,
        le=100
    )

    quantity_score: float = Field(
        ge=0,
        le=100
    )

    evidence_score: float = Field(
        ge=0,
        le=100
    )

    delivery_score: float = Field(
        ge=0,
        le=100
    )

    score_reasoning: list[str]

    risks: list[str]

    recommended_next_step: str