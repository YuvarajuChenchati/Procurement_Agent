def classify_geography(
    vendor_location: str | None,
    vendor_country: str | None,
    procurement_city: str,
    procurement_country: str,
):

    if not vendor_country:
        return "unknown"

    country = vendor_country.lower().strip()

    procurement_country = (
        procurement_country.lower().strip()
    )

    if country != procurement_country:
        return "global"

    if not vendor_location:
        return "unknown"

    location = vendor_location.lower().strip()

    city = procurement_city.lower().strip()

    if city in location:
        return "ahmedabad"

    return "india"