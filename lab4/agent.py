from langchain.agents import create_structured_chat_agent, AgentExecutor
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain import hub
from tools import (
    get_current_weather,
    get_weather_forecast,
    search_flights,
    search_hotels,
)
import os
from dotenv import load_dotenv
load_dotenv()


def create_agent():
    # LLM
    llm = ChatGoogleGenerativeAI(
        model="gemini-flash-latest",
        temperature=0.3,
        google_api_key=os.getenv("GOOGLE_API_KEY"),
    )

    tools = [
        get_current_weather,
        get_weather_forecast,
        search_flights,
        search_hotels,
    ]

    # Prompt from LangChain hub
    prompt = hub.pull("hwchase17/structured-chat-agent")

    agent = create_structured_chat_agent(llm, tools, prompt)

    agent_executor = AgentExecutor(
        agent=agent,
        tools=tools,
        verbose=True,
        handle_parsing_errors=True   # <-- ADD THIS
    )

    return agent_executor
