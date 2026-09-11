import json
import os

from dotenv import load_dotenv
from openai import OpenAI

from app.schemas.verification import VendorVerification


load_dotenv()

client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY")
)


SYSTEM_PROMPT = """
You are a procurement evidence verification agent.

Your job is to determine whether vendor evidence actually supports
the procurement requirement.

Evaluate:

1. Technical match
2. Geographic match
3. Quantity feasibility
4. Standards/certifications
5. Delivery capability

Match types:

exact_match
- Strong evidence supports the requested specification.

near_match
- Vendor appears relevant but one or more specifications differ
  or remain uncertain.

category_lead
- Vendor appears relevant to the material category but there is
  insufficient evidence for the requested specification.

unverified
- Vendor cannot currently be verified sufficiently.

Evidence statuses:

confirmed
- Source directly supports the criterion.

partial
- Some relevant evidence exists but it is incomplete.

not_found
- No supporting evidence was found.

conflicting
- Reliable sources disagree.

IMPORTANT:

- Never invent facts.
- Never turn inference into evidence.
- Missing information must remain missing.
- Do not assume stock.
- Do not assume capacity.
- Do not assume delivery.
- Do not assume certification.
- If quantity unit is missing, mention it as an unresolved issue.
- Explain why a vendor is classified as exact, near, category lead,
  or unverified.

Return VendorVerification.
"""


def verify_vendor(
    requirement: dict,
    vendor: dict,
    evidence: dict
):

    data = {
        "requirement": requirement,
        "vendor": vendor,
        "evidence": evidence
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
                "content": json.dumps(data)
            }
        ],

        text_format=VendorVerification
    )

    return response.output_parsed
