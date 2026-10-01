import os

from dotenv import load_dotenv
from openai import OpenAI


load_dotenv()

XAI_API_KEY = os.getenv("XAI_API_KEY")

if not XAI_API_KEY:
    raise RuntimeError("XAI_API_KEY is not set in the .env file")


client = OpenAI(
    api_key=XAI_API_KEY,
    base_url="https://api.x.ai/v1"
)


def ask_grok(prompt: str) -> str:
    response = client.chat.completions.create(
        model="grok-4.1-fast",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ],
    )

    return response.choices[0].message.content