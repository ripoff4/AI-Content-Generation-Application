from tavily import TavilyClient
from dotenv import load_dotenv
from backend.config import ARTICLE_AGE
import os

load_dotenv()

client = TavilyClient(
    api_key=os.getenv("TAVILY_API_KEY")
)


def get_trending_information(topic: str):

    enhanced_query = (
        f"Latest trending news and viral discussions "
        f"about {topic}"
    )

    response = client.search(
        query=enhanced_query,
        search_depth="advanced",
        max_results=10,
        topic="news",
        days=ARTICLE_AGE,
        include_answer=False,
        include_raw_content=False
    )

    results = response.get("results", [])

    extracted_results = []

    for result in results:

        extracted_results.append({
            "title": result.get("title", ""),
            "content": result.get("content", ""),
            "url": result.get("url", ""),
            "published_date": result.get("published_date", "Unknown")
        })

    return extracted_results
