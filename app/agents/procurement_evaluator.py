import json
import os

from dotenv import load_dotenv
from openai import OpenAI

from app.schemas.evaluation import ProcurementEvaluation

load_dotenv()

client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY")
)


SYSTEM_PROMPT = """
You are a procurement evaluation agent.

Evaluate a vendor using ONLY the supplied requirement
and verified vendor evidence.

Score each criterion from 0 to 100.

Technical score:
- 0: no evidence of technical suitability
- 50: partial or near match
- 100: strong evidence of technical match

Geographic score:
- 0: geography unsuitable or unknown
- 50: potentially suitable
- 100: clearly suitable for procurement location

Quantity score:
- 0: no relevant bulk evidence
- 50: supplier appears relevant but quantity capability is unverified
- 100: strong evidence of bulk quantity capability

Evidence score:
- 0: weak evidence
- 50: moderate evidence
- 100: strong primary-source evidence

Delivery score:
- 0: no delivery/service evidence
- 50: potentially capable
- 100: clear delivery/service evidence

IMPORTANT:

- Never invent facts.
- Missing evidence must receive a conservative score.
- Never assume stock.
- Never assume capacity.
- Never assume delivery time.
- Never assume certification.
- Never convert an assumption into a fact.
- If quantity unit is missing, explicitly mention this limitation.
- Explain the reasoning behind the scores.

Return the required structured output.
"""


def evaluate_vendor(
    requirement: dict,
    verification: dict
):

    data = {
        "requirement": requirement,
        "verification": verification
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

        text_format=ProcurementEvaluation
    )

    return response.output_parsed
