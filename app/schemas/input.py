from typing import Optional

from pydantic import BaseModel


class Location(BaseModel):
    city: str
    state: str
    country: str


class ProcurementRequest(BaseModel):
    id: str
    material: str
    quantity: float
    quantity_unit: Optional[str] = None
    location: Location