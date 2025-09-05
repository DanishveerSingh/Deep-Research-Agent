from agents import Agent, WebSearchTool, ModelSettings, OpenAIChatCompletionsModel
from dotenv import load_dotenv
from openai import AsyncOpenAI
import os

load_dotenv(override=True)

openai_api_key = os.getenv('OPENAI_API_KEY')
openrouter_api_key = os.getenv('OPENROUTER_API_KEY')
openrouter_base_url = "https://openrouter.ai/api/v1"
openrouter_client = AsyncOpenAI(base_url=openrouter_base_url, api_key=openrouter_api_key)
openrouter_model = OpenAIChatCompletionsModel(model = "google/gemini-2.0-flash-001", openai_client=openrouter_client)

INSTRUCTIONS = (
    "You are a research assistant. Given a search term, you search the web for that term and "
    "produce a concise summary of the results. The summary must 2-3 paragraphs and less than 300 "
    "words. Capture the main points. Write succintly, no need to have complete sentences or good "
    "grammar. This will be consumed by someone synthesizing a report, so its vital you capture the "
    "essence and ignore any fluff. Do not include any additional commentary other than the summary itself."
)

search_agent = Agent(
    name="Search agent",
    instructions=INSTRUCTIONS,
    tools=[WebSearchTool(search_context_size="low")],
    model=openrouter_model,
    model_settings=ModelSettings(tool_choice="required"),
)