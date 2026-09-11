import re
from urllib.parse import urlparse


def get_domain(url: str | None) -> str | None:
    if not url:
        return None
    try:
        return urlparse(url).netloc.lower().removeprefix("www.") or None
    except (TypeError, ValueError):
        return None


def normalize_vendor_name(name: str) -> str:

    name = name.lower().strip()

    name = re.sub(r"[^\w\s]", " ", name)

    name = re.sub(r"\s+", " ", name)

    suffixes = [
        "private limited",
        "pvt ltd",
        "pvt limited",
        "limited",
        "ltd",
        "llp",
    ]

    for suffix in suffixes:
        if name.endswith(" " + suffix):
            name = name[: -len(suffix)].strip()

    return name


def deduplicate_vendors(vendors: list[dict]) -> list[dict]:

    unique_vendors = {}

    for vendor in vendors:

        normalized_name = normalize_vendor_name(vendor["vendor_name"])
        domain = get_domain(vendor.get("website")) or get_domain((vendor.get("source_urls") or [None])[0])
        location = (vendor.get("location") or "").lower().strip()
        identity = (normalized_name, domain, location) if domain or location else (normalized_name, None, None)

        if identity not in unique_vendors:

            unique_vendors[identity] = vendor

        else:

            existing = unique_vendors[identity]

            # Merge evidence
            existing["product_evidence"] = list(
                set(
                    existing.get("product_evidence", [])
                    + vendor.get("product_evidence", [])
                )
            )

            # Merge source URLs
            existing["source_urls"] = list(
                set(
                    existing.get("source_urls", [])
                    + vendor.get("source_urls", [])
                )
            )

    return list(unique_vendors.values())
