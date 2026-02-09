from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.agents import initialize_agent, AgentType
from dotenv import load_dotenv
from tools import (
    get_current_weather,
    get_weather_forecast,
    search_flights,
    search_hotels,
)

load_dotenv()

def create_agent():
    llm = ChatGoogleGenerativeAI(
        model="gemini-pro",
        temperature=0.4
    )

    tools = [
        get_current_weather,
        get_weather_forecast,
        search_flights,
        search_hotels,
    ]

    agent = initialize_agent(
        tools=tools,
        llm=llm,
        agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
        verbose=True
    )

    return agent
