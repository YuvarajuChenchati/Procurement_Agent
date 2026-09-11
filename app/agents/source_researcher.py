import json
import os

from dotenv import load_dotenv
from openai import OpenAI

from app.schemas.evidence import VendorEvidence


load_dotenv()

client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY")
)


SYSTEM_PROMPT = """
You are a procurement source research agent.

Investigate a vendor using web sources.

Evaluate evidence for:

1. Product/material
2. Exact specifications
3. Standards
4. Geography
5. Quantity/capacity/bulk ordering
6. Delivery/service area

IMPORTANT:

- Prefer official vendor websites.
- Never invent facts.
- Never assume stock.
- Never assume capacity.
- Never assume delivery capability.
- Never assume certification.
- Never infer exact dimensions from generic product descriptions.
- If information cannot be found, use "not_found".
- If sources disagree, use "conflicting".
- Preserve source URLs.
- Keep evidence tied to its source.
- Search-result context is not proof of a claim.

Reliability:

official vendor source:
high

manufacturer documentation:
high

established industry source:
medium

directory/marketplace:
low or medium

Return the required VendorEvidence structure.
"""


def research_vendor(
    requirement: dict,
    vendor: dict
):

    user_input = {
        "requirement": requirement,
        "vendor": vendor
    }

    response = client.responses.parse(
        model="gpt-5.6-luna",

        tools=[
            {
                "type": "web_search"
            }
        ],

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

        text_format=VendorEvidence
    )

    return response.output_parsed
