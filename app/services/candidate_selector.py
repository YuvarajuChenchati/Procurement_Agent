"""Keep expensive evidence research bounded and geographically balanced."""


def select_candidates(vendors: list[dict], limit_per_category: int = 5) -> list[dict]:
    """Select at most the requested number of candidates per geography."""
    categories = {"ahmedabad": [], "india": [], "global": [], "unknown": []}
    for vendor in vendors:
        category = vendor.get("geographic_category", "unknown")
        categories.get(category, categories["unknown"]).append(vendor)
    return [vendor for category in categories.values() for vendor in category[:limit_per_category]]
