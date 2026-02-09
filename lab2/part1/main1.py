from dataclasses import dataclass
import os

from dotenv import load_dotenv
from langchain.agents import create_agent
from langchain.tools import tool
from langchain.agents.structured_output import ToolStrategy
from langgraph.checkpoint.memory import InMemorySaver
from langchain_openai import ChatOpenAI

# -------------------------------------------------
# ENV SETUP
# -------------------------------------------------
load_dotenv()

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
if not OPENROUTER_API_KEY:
    raise ValueError("OPENROUTER_API_KEY not found in .env file")

# -------------------------------------------------
# MODEL CONFIG
# -------------------------------------------------
model = ChatOpenAI(
    model="openai/gpt-4o-mini",
    api_key=OPENROUTER_API_KEY,
    base_url="https://openrouter.ai/api/v1",
    temperature=0.3
)

# -------------------------------------------------
# SYSTEM PROMPT (STRICT & DETERMINISTIC)
# -------------------------------------------------
SYSTEM_PROMPT = """You are a college helpdesk assistant.

Rules (must follow):
- You MUST use the get_college_info tool for every question
- Use the tool output to answer
- ALWAYS set source to "college helpdesk"
- Be clear and concise
"""

# -------------------------------------------------
# CONTEXT SCHEMA
# -------------------------------------------------
@dataclass
class Context:
    user_id: str

# -------------------------------------------------
# TOOL
# -------------------------------------------------
@tool
def get_college_info(topic: str) -> str:
    """Get basic college-related information."""
    data = {
        "attendance": "Minimum 75% attendance is required to appear for exams.",
        "exam": "End semester exams are conducted in December and May.",
        "library": "The college library is open from 9 AM to 8 PM on weekdays.",
        "fees": "Semester fees must be paid within the first month.",
        "hostel": "Hostel curfew time is 10 PM for all students."
    }
    return data.get(
        topic.lower(),
        "Sorry, I don't have information on that topic."
    )

# -------------------------------------------------
# RESPONSE FORMAT (NO OPTIONAL FIELDS)
# -------------------------------------------------
@dataclass
class ResponseFormat:
    answer: str
    source: str

# -------------------------------------------------
# MEMORY
# -------------------------------------------------
checkpointer = InMemorySaver()

# -------------------------------------------------
# CREATE AGENT
# -------------------------------------------------
agent = create_agent(
    model=model,
    system_prompt=SYSTEM_PROMPT,
    tools=[get_college_info],
    context_schema=Context,
    response_format=ToolStrategy(ResponseFormat),
    checkpointer=checkpointer
)

# -------------------------------------------------
# RUN AGENT
# -------------------------------------------------
config = {"configurable": {"thread_id": "1"}}

# FIRST QUESTION (explicit)
response = agent.invoke(
    {
        "messages": [
            {"role": "user", "content": "Tell me about attendance"}
        ]
    },
    config=config,
    context=Context(user_id="1")
)

print("\nResponse 1:")
print(response["structured_response"])

# SECOND QUESTION (explicit – no ambiguity)
response = agent.invoke(
    {
        "messages": [
            {"role": "user", "content": "Tell me about exams"}
        ]
    },
    config=config,
    context=Context(user_id="1")
)

print("\nResponse 2:")
print(response["structured_response"])
