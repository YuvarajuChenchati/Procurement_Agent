"""Manual smoke test for web-search evidence extraction.

Run from the repository root: ``python tests/test_search.py``.
This makes a live API call and therefore requires OPENAI_API_KEY.
"""

from app.tools.web_search import web_search


if __name__ == "__main__":
    response = web_search("ERW pipe IS 1239 60.3 x 5.5 mm Ahmedabad supplier")
    print("SOURCES")
    print("=" * 50)
    for source in response["sources"]:
        print(f"\nTitle: {source['title']}")
        print(f"URL: {source['url']}")
    print("\nSEARCH TEXT")
    print("=" * 50)
    print(response["text"])
