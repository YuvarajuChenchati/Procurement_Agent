import os

from dotenv import load_dotenv
from openai import OpenAI


load_dotenv()

client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY")
)


def web_search(query: str):

    response = client.responses.create(
        model="gpt-5.6-luna",
        tools=[
            {
                "type": "web_search"
            }
        ],
        include=[
            "web_search_call.action.sources"
        ],
        input=query,
    )

    sources = []

    # Extract citations from model output
    for output_item in response.output:

        if not hasattr(output_item, "content"):
            continue

        for content_item in output_item.content:

            if not hasattr(content_item, "annotations"):
                continue

            for annotation in content_item.annotations:

                if getattr(annotation, "type", None) == "url_citation":

                    sources.append({
                        "title": annotation.title,
                        "url": annotation.url
                    })

    # Remove duplicate URLs
    unique_sources = {}

    for source in sources:
        unique_sources[source["url"]] = source

    return {
        "query": query,
        "text": response.output_text,
        "sources": list(unique_sources.values()),
    }