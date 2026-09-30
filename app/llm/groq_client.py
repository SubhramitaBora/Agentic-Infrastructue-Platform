import os

from dotenv import load_dotenv
from groq import AsyncGroq

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
GROQ_MODEL = os.getenv("GROQ_MODEL", "qwen/qwen3-32b")

if not GROQ_API_KEY:
    raise RuntimeError("GROQ_API_KEY is not configured.")

client = AsyncGroq(api_key=GROQ_API_KEY)


async def ask_groq(prompt: str) -> str:

    response = await client.chat.completions.create(
        model=GROQ_MODEL,
        messages=[
            {
                "role": "user",
                "content": prompt,
            }
        ],
        temperature=0,
    )

    return response.choices[0].message.content


async def chat_with_groq(messages: list[dict], tools: list[dict]):
    """Create one tool-aware chat completion for the agent loop."""
    return await client.chat.completions.create(
        model=GROQ_MODEL,
        messages=messages,
        tools=tools,
        tool_choice="auto",
        parallel_tool_calls=False,
        temperature=0,
    )
