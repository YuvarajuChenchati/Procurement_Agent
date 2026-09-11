import json
import os

from dotenv import load_dotenv
from openai import OpenAI

from app.schemas.report import ProcurementReport


load_dotenv()

client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY")
)


SYSTEM_PROMPT = """
You are a procurement report generation agent.

Your task is to create the final procurement report from:

1. Original procurement requirement
2. Requirement analysis
3. Vendor information
4. Vendor verification
5. Vendor evaluation and ranking

The report must be evidence-based.

IMPORTANT RULES:

- Preserve the original requirement.
- Preserve ambiguities.
- Preserve assumptions.
- Never invent vendor information.
- Never invent stock.
- Never invent capacity.
- Never invent price.
- Never invent delivery time.
- Never invent certifications.
- Never convert assumptions into facts.
- Clearly distinguish evidence from inference.
- Keep unresolved issues visible.
- Include failed searches in search_issues with query and reason; do not silently hide them.
- Keep source URLs.
- Include a website and public contact details only when they appear in the supplied evidence.
- Separate vendors into:
    - Ahmedabad
    - India
    - Global
    - Excluded or unverified

Match types must be:

- exact_match
- near_match
- category_lead
- unverified

Confidence must be:

- high
- medium
- low

Recommendation status must be one of:
- shortlist_candidate: suitable for RFQ/technical follow-up, never procurement approval.
- needs_verification: relevant but material evidence remains missing.
- unverified: insufficient evidence or a failed verification.

The report should help a procurement person decide:

1. Which vendors deserve further consideration?
2. Why were they included?
3. What evidence supports them?
4. What is still unverified?
5. What should procurement do next?

Return the required structured report.
"""


def generate_report(
    request: dict,
    analysis: dict,
    vendors: list,
    verifications: list,
    rankings: list,
    search_results: list | None = None,
):

    data = {
        "request": request,
        "analysis": analysis,
        "vendors": vendors,
        "verifications": verifications,
        "rankings": rankings,
        "search_results": search_results or [],
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
        text_format=ProcurementReport
    )

    return response.output_parsed
