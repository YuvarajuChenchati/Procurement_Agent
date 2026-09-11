from typing import TypedDict


class ProcurementState(TypedDict, total=False):

    request: dict

    analysis: dict

    search_queries: dict

    search_results: list

    vendors: list

    evidence: list

    verifications: list

    evaluations: list

    rankings: list

    final_report: dict