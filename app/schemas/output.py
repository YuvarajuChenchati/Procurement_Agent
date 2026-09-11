from typing import List, Optional, Literal
from pydantic import BaseModel

from app.schemas.input import ProcurementRequest


class Ambiguity(BaseModel):
    field: str
    issue: str
    severity: Literal["low", "medium", "high"]


class NormalizedRequirement(BaseModel):
    material_type: Optional[str] = None
    nominal_diameter: Optional[str] = None
    outer_diameter: Optional[str] = None
    wall_thickness: Optional[str] = None
    standard: Optional[str] = None
    grade: Optional[str] = None
    pipe_class: Optional[str] = None


class RequirementAnalysis(BaseModel):
    original_requirement: ProcurementRequest
    normalized_requirement: NormalizedRequirement
    ambiguities: List[Ambiguity]
    assumptions: List[str]
