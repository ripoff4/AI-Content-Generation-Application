from langgraph.graph import StateGraph, START, END
from typing import TypedDict
from langchain_openai import ChatOpenAI
from tenacity import retry, stop_after_attempt, wait_fixed

from backend.ingestion.tavily import get_trending_information
from backend.ingestion.reddit import get_reddit_trending_information

from backend.config import ARTICLE_AGE, LIMIT

import os
from dotenv import load_dotenv

load_dotenv()


class AgentState(TypedDict):

    user_question: str

    response: str

    extracted_information: list

    reddit_extracted_information: list


llm = ChatOpenAI(
    model="gpt-4o-mini",
    api_key=os.getenv("OPENAI_API_KEY"),
    temperature=0
)


@retry(
    stop=stop_after_attempt(3),
    wait=wait_fixed(2)
)
def get_extracted_information(state: AgentState):

    results = get_trending_information(
        state["user_question"]
    )

    topic = state["user_question"].lower()

    filtered_results = []

    for result in results:

        combined_text = (
            result["title"] + " " +
            result["content"]
        ).lower()

        if topic in combined_text.lower():

            filtered_results.append(result)

    return {
        "extracted_information": filtered_results
    }


@retry(
    stop=stop_after_attempt(3),
    wait=wait_fixed(2)
)
def get_reddit_extracted_information(state: AgentState):

    reddit_query = llm.invoke(
        f"""
        Convert this topic into a short Reddit search query.

        Topic:
        {state['user_question']}

        Rules:
        - Keep it short
        - 1 to 3 words maximum
        - No explanation
        - No punctuation
        """
    ).content.strip()

    results = get_reddit_trending_information(
        reddit_query,
        days=ARTICLE_AGE,
        limit=LIMIT
    )

    topic = state["user_question"].lower()

    filtered_results = []

    for result in results:

        combined_text = (
            result["title"] + " " +
            result["content"]
        ).lower()

        if topic in combined_text.lower():

            filtered_results.append(result)

    return {
        "reddit_extracted_information": filtered_results
    }


def summarize_information(state: AgentState):

    informations = state["extracted_information"]

    reddit_information = state[
        "reddit_extracted_information"
    ]

    if not informations and not reddit_information:

        return {
            "response": (
                f"No recent trending information found "
                f"for '{state['user_question']}'."
            )
        }

    tavily_contents = "\n\n".join(
        [
            f"""
            NEWS ARTICLE {i+1}

            Title: {info['title']}

            Published Date:
            {info['published_date']}

            Content:
            {info['content']}
            """
            for i, info in enumerate(informations)
        ]
    )

    reddit_contents = "\n\n".join(
        [
            f"""
            REDDIT POST {i+1}

            Title:
            {post['title']}

            Subreddit:
            r/{post['subreddit']}

            Upvotes:
            {post['score']}

            Content:
            {post['content']}
            """
            for i, post in enumerate(
                reddit_information
            )
        ]
    )

    prompt = f"""
    You are a real-time internet trend analyst.

    You are given TWO types of data:

    1. NEWS DATA
    - factual reporting
    - announcements
    - mainstream coverage

    2. REDDIT COMMUNITY DATA
    - fan reactions
    - emotional discussions
    - memes
    - hype
    - controversies
    - internet sentiment

    IMPORTANT:
    - Ignore outdated information
    - Focus ONLY on currently active discussions
    - Prioritize highly engaging trends
    - Avoid generic summaries
    - Do NOT explain background/history
    - Focus on WHAT is trending and WHY

    NEWS DATA:
    {tavily_contents}

    REDDIT DATA:
    {reddit_contents}

    USER TOPIC:
    {state["user_question"]}

    OUTPUT FORMAT:

    1. <Trend insight>

    2. <Trend insight>

    3. <Trend insight>

    4. <Trend insight>

    Rules:
    - 2-4 sentences each
    - concise
    - engaging
    - modern internet tone
    - mention reactions/sentiment
    - explain WHY people care
    """

    response = llm.invoke(prompt)

    return {
        "response": response.content
    }


graph = StateGraph(AgentState)

graph.add_node(
    "get_extracted_information",
    get_extracted_information
)

graph.add_node(
    "get_reddit_extracted_information",
    get_reddit_extracted_information
)

graph.add_node(
    "summarize_information",
    summarize_information
)

graph.add_edge(
    START,
    "get_extracted_information"
)

graph.add_edge(
    "get_extracted_information",
    "get_reddit_extracted_information"
)

graph.add_edge(
    "get_reddit_extracted_information",
    "summarize_information"
)

graph.add_edge(
    "summarize_information",
    END
)

agent = graph.compile()
