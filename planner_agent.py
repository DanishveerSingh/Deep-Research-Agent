from pydantic import BaseModel, Field
from agents import Agent, OpenAIChatCompletionsModel
from dotenv import load_dotenv
from openai import AsyncOpenAI
import os

load_dotenv(override=True)

openai_api_key = os.getenv('OPENAI_API_KEY')
openrouter_api_key = os.getenv('OPENROUTER_API_KEY')
openrouter_base_url = "https://openrouter.ai/api/v1"
openrouter_client = AsyncOpenAI(base_url=openrouter_base_url, api_key=openrouter_api_key)
openrouter_model = OpenAIChatCompletionsModel(model = "google/gemini-2.0-flash-001", openai_client=openrouter_client)

HOW_MANY_SEARCHES = 3

INSTRUCTIONS = f"You are a helpful research assistant. Given a query, come up with a set of web searches \
to perform to best answer the query. Output {HOW_MANY_SEARCHES} terms to query for."


class WebSearchItem(BaseModel):
    reason: str = Field(description="Your reasoning for why this search is important to the query.")
    query: str = Field(description="The search term to use for the web search.")


class WebSearchPlan(BaseModel):
    searches: list[WebSearchItem] = Field(description="A list of web searches to perform to best answer the query.")
    
planner_agent = Agent(
    name="PlannerAgent",
    instructions=INSTRUCTIONS,
    model=openrouter_model,
    output_type=WebSearchPlan,
)