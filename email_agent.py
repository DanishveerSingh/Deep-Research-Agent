import os
from typing import Dict
import sendgrid
from sendgrid.helpers.mail import Email, Mail, Content, To
from agents import Agent, function_tool, OpenAIChatCompletionsModel
from dotenv import load_dotenv
from openai import AsyncOpenAI

load_dotenv(override=True)

openai_api_key = os.getenv('OPENAI_API_KEY')
openrouter_api_key = os.getenv('OPENROUTER_API_KEY')
openrouter_base_url = "https://openrouter.ai/api/v1"
openrouter_client = AsyncOpenAI(base_url=openrouter_base_url, api_key=openrouter_api_key)
openrouter_model = OpenAIChatCompletionsModel(model = "google/gemini-2.0-flash-001", openai_client=openrouter_client)

@function_tool
def send_email(subject: str, html_body: str) -> Dict[str, str]:
    """ Send an email with the given subject and HTML body """
    sg = sendgrid.SendGridAPIClient(api_key=os.environ.get('SENDGRID_API_KEY'))
    from_email = Email("danishveersingh2004@gmail.com") 
    to_email = To("dsingh3_be23@thapar.edu")
    content = Content("text/html", html_body)
    mail = Mail(from_email, to_email, subject, content).get()
    response = sg.client.mail.send.post(request_body=mail)
    print("Email response", response.status_code)
    return {"status": "success"}

INSTRUCTIONS = """You are able to send a nicely formatted HTML email based on a detailed report.
You will be provided with a detailed report. You should use your tool to send one email, providing the 
report converted into clean, well presented HTML with an appropriate subject line."""

email_agent = Agent(
    name="Email agent",
    instructions=INSTRUCTIONS,
    tools=[send_email],
    model=openrouter_model,
)
