import httpx

from app.config import (
    HYDRA_LITELLM_BASE_URL,
    HYDRA_API_KEY,
    HYDRA_MODEL,
    HYDRA_TIMEOUT,
)


async def ask_hydra(prompt: str) -> str:
    """
    Send a prompt to the Hydra LiteLLM Gateway
    and return the model's response.
    """

    url = f"{HYDRA_LITELLM_BASE_URL.rstrip('/')}/chat/completions"

    headers = {
        "Content-Type": "application/json",
    }

    if HYDRA_API_KEY:
        headers["Authorization"] = f"Bearer {HYDRA_API_KEY}"

    payload = {
        "model": HYDRA_MODEL,
        "messages": [
            {
                "role": "user",
                "content": prompt,
            }
        ],
    }

    async with httpx.AsyncClient(
        timeout=HYDRA_TIMEOUT
    ) as client:

        response = await client.post(
            url,
            headers=headers,
            json=payload,
        )

        response.raise_for_status()

        data = response.json()

    return data["choices"][0]["message"]["content"]