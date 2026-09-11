import json
import os

from dotenv import load_dotenv
from openai import OpenAI
from pydantic import BaseModel, Field

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


class SearchQueryPlan(BaseModel):
    """A bounded, validated search plan instead of free-form JSON text."""
    ahmedabad: list[str] = Field(min_length=1, max_length=4)
    india: list[str] = Field(min_length=1, max_length=4)
    global_: list[str] = Field(alias="global", min_length=1, max_length=4)


SYSTEM_PROMPT = """
You are a procurement web research agent.

Your job is to create targeted web-search queries
for finding industrial material suppliers.

You will receive a normalized procurement requirement.

Generate searches for THREE geographic categories:

1. Ahmedabad
   - Vendors located in Ahmedabad
   - Ahmedabad manufacturers
   - Ahmedabad suppliers/stockists
   - Ahmedabad warehouses or local supply

2. India
   - Vendors elsewhere in India
   - Manufacturers and suppliers
   - Vendors capable of supplying/delivering to Ahmedabad

3. Global
   - Vendors outside India
   - International manufacturers/suppliers
   - Vendors that may potentially export to India

Rules:

- Preserve the technical specifications exactly.
- Do not invent missing specifications.
- Do not invent quantity units.
- Do not assume a technical ambiguity has been resolved.
- Generate concise, useful search queries.
- Search queries should contain relevant material specifications.
- Generate multiple queries for each geographic category.

Return ONLY valid JSON in this format:

{
  "ahmedabad": ["query 1", "query 2"],
  "india": ["query 1", "query 2"],
  "global": ["query 1", "query 2"]
}
"""


def generate_search_queries(requirement: dict) -> dict[str, list[str]]:

    response = client.responses.parse(
        model="gpt-5.6-luna",
        input=[
            {
                "role": "system",
                "content": SYSTEM_PROMPT
            },
            {
                "role": "user",
                "content": json.dumps(requirement)
            }
        ],
        text_format=SearchQueryPlan,
    )

    return response.output_parsed.model_dump(by_alias=True)
