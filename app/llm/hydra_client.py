import httpx

from app.config import (
    HYDRA_LITELLM_BASE_URL,
    HYDRA_API_KEY,
    HYDRA_MODEL,
    HYDRA_TIMEOUT,
)


async def ask_hydra(prompt: str) -> str:

    print(f"Hydra URL: {HYDRA_LITELLM_BASE_URL}", flush=True)
    print(f"Hydra model: {HYDRA_MODEL}", flush=True)

    if not HYDRA_LITELLM_BASE_URL:
        raise RuntimeError("HYDRA_LITELLM_BASE_URL is not configured.")

    if not HYDRA_MODEL:
        raise RuntimeError("HYDRA_MODEL is not configured.")

    url = (
        f"{HYDRA_LITELLM_BASE_URL.rstrip('/')}"
        "/chat/completions"
    )

    print(f"Sending POST request to: {url}", flush=True)

    headers = {
        "Content-Type": "application/json"
    }

    if HYDRA_API_KEY:
        headers["Authorization"] = f"Bearer {HYDRA_API_KEY}"

    payload = {
        "model": HYDRA_MODEL,
        "messages": [
            {
                "role": "user",
                "content": prompt
            }
        ],
    }

    async with httpx.AsyncClient(
        timeout=HYDRA_TIMEOUT
    ) as client:

        print("Waiting for Hydra response...", flush=True)

        response = await client.post(
            url,
            headers=headers,
            json=payload,
        )

        print(
            f"Hydra HTTP status: {response.status_code}",
            flush=True
        )

        response.raise_for_status()

        data = response.json()

    return data["choices"][0]["message"]["content"]