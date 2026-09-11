import json
import os

from dotenv import load_dotenv
from openai import OpenAI

from app.schemas.output import RequirementAnalysis


load_dotenv()

client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY")
)


SYSTEM_PROMPT = """
You are a procurement requirement analysis agent.

Analyze industrial material requirements.

Your responsibilities:

1. Preserve the original requirement.
2. Extract only specifications explicitly provided.
3. Normalize the technical information.
4. Detect missing information.
5. Detect technical ambiguities.
6. Record assumptions separately.
7. Never invent dimensions, standards, quantities,
   stock, certifications, prices, lead times or capacity.
8. If quantity unit is missing, identify it as an ambiguity.
9. Do not silently modify the user's requirement.

Return the information using the required structured schema.
"""


def analyze_requirement(request: dict):

    response = client.responses.parse(
        model="gpt-5.6-luna",

        input=[
            {
                "role": "system",
                "content": SYSTEM_PROMPT
            },
            {
                "role": "user",
                "content": json.dumps(request)
            }
        ],

        text_format=RequirementAnalysis
    )

    return response.output_parsed
