import json
import os

from dotenv import load_dotenv
from openai import OpenAI
from pydantic import BaseModel, Field

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


class VendorExtraction(BaseModel):
    vendors: list[dict] = Field(default_factory=list)


SYSTEM_PROMPT = """
You are a procurement vendor extraction agent.

Your task is to identify potential vendors from web research results.

For each result:

1. Determine whether it represents an actual vendor.
2. Extract the vendor/company name.
3. Extract location if explicitly available.
4. Extract country if explicitly available.
5. Identify vendor type if supported by evidence.
6. Extract product/specification evidence.
7. Extract the website/source URL.
8. Extract public contact details only when explicitly shown on the source.
8. Assign the geographic category provided by the caller.

Important rules:

- Do not invent information.
- Do not treat a generic product page as a vendor unless a company/vendor is identifiable.
- Do not assume a vendor's location.
- Do not claim a vendor manufactures a product unless the source supports it.
- Do not claim stock, capacity, price, lead time or certification unless supported.
- Preserve uncertainty.
- A search result is evidence, not proof of suitability.

Return ONLY valid JSON.

Format:

{
    "vendors": [
        {
            "vendor_name": "...",
            "location": "...",
            "country": "...",
            "vendor_type": "...",
            "website": "...",
            "contact_details": ["phone or public email, if sourced"],
            "product_evidence": ["..."],
            "source_urls": ["..."],
            "geographic_category": "...",
            "confidence": "low"
        }
    ]
}
"""


def extract_vendors(search_results, geographic_category) -> list[dict]:

    user_input = {
        "geographic_category": geographic_category,
        "search_results": search_results
    }

    response = client.responses.parse(
        model="gpt-5.6-luna",
        input=[
            {
                "role": "system",
                "content": SYSTEM_PROMPT
            },
            {
                "role": "user",
                "content": json.dumps(user_input)
            }
        ],
        text_format=VendorExtraction,
    )

    return response.output_parsed.vendors
