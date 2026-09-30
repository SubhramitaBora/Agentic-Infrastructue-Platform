import asyncio

from app.llm.hydra_client import ask_hydra


async def main():
    print("Testing Hydra connection...", flush=True)

    try:
        print("Sending request to Hydra...", flush=True)

        response = await asyncio.wait_for(
            ask_hydra(
                "Respond with exactly: Hydra connection successful."
            ),
            timeout=30,
        )

        print("\nHydra response:", flush=True)
        print(response, flush=True)

        print("\nHydra connection test PASSED.", flush=True)

    except asyncio.TimeoutError:
        print("\nERROR: Hydra request timed out after 30 seconds.", flush=True)
        print("Check the Hydra/LiteLLM URL, network access, and whether the model is running.", flush=True)

    except Exception as e:
        print("\nHydra connection test FAILED.", flush=True)
        print(f"Error type: {type(e).__name__}", flush=True)
        print(f"Error: {e}", flush=True)


if __name__ == "__main__":
    asyncio.run(main())