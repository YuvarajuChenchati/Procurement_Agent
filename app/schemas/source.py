from typing import Literal
from pydantic import BaseModel


class Source(BaseModel):

    title: str

    url: str

    source_type: Literal[
        "official_vendor",
        "manufacturer",
        "industry_directory",
        "marketplace",
        "other"
    ]

    evidence: str

    reliability: Literal[
        "high",
        "medium",
        "low"
    ]