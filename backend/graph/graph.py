from langgraph.graph import StateGraph, START, END
from langchain.tools import tool
from typing import TypedDict
from langchain_community.tools.tavily_search import TavilySearchResults
from langchain_openai import ChatOpenAI

import os
from dotenv import load_dotenv

load_dotenv()


class AgentState(TypedDict):

    user_question: str
    response: str
    extracted_information: list


llm = ChatOpenAI(
    model="gpt-4o-mini",
    api_key=os.getenv("OPENAI_API_KEY"),
    temperature=0
)


@tool
def get_trending_information(user_question: str):
    '''
        This is called Everysingle Time the graph is called    
        This Tool is used to get trending information.
    '''
    search_tool = TavilySearchResults(max_results=3)
    results = search_tool.invoke(user_question)
    return results


def get_extracted_information(state: AgentState) -> AgentState:

    results = get_trending_information.invoke(
        {"user_question": state["user_question"]})

    return {"extracted_information": results}


def summarize_information(state: AgentState) -> AgentState:

    informations = state["extracted_information"]

    titles = "\n".join(
        [f"- {info['title']}" for info in informations]
    )

    contents = "\n\n".join(
        [f"{i+1}. {info['content']}" for i, info in enumerate(informations)]
    )

    prompt = prompt = f"""
        You are a real-time internet trend analyst.

        Your job is to analyze web search results and identify:
        - what is currently trending
        - what people are discussing heavily
        - viral moments
        - controversies
        - major announcements
        - surprising developments
        - emotional audience reactions
        - hype-worthy topics

        IMPORTANT RULES:
        - DO NOT generate a generic article.
        - DO NOT explain background/history unless absolutely necessary.
        - DO NOT give educational content.
        - Focus ONLY on current trending discussions and recent buzz.
        - The response should feel like insights collected from social media,
        news discussions, YouTube commentary, Reddit, and fan conversations.
        - Mention specific names, events, incidents, launches, matches,
        performances, statements, or controversies whenever possible.
        - Keep each trend short, engaging, and information-dense.
        - Avoid corporate or textbook tone.

        WEB SEARCH RESULTS:
        {contents}

        USER TOPIC:
        {state["user_question"]}

        OUTPUT FORMAT:

        1. <Trend insight>

        2. <Trend insight>

        3. <Trend insight>

        4. <Trend insight>

        Each point should:
        - be 2-4 sentences
        - explain WHY it is trending
        - mention what people are reacting to
        - feel current and engaging
    """

    response = llm.invoke(prompt)

    return {"response": response.content}


graph = StateGraph(AgentState)

graph.add_node("get_extracted_information", get_extracted_information)
graph.add_node("summarize_information", summarize_information)

graph.add_edge(START, "get_extracted_information")
graph.add_edge("get_extracted_information", "summarize_information")
graph.add_edge("summarize_information", END)

agent = graph.compile()
