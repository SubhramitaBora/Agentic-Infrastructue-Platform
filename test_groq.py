import asyncio

from app.llm.groq_client import ask_groq


async def main():

    print("Testing Groq connection...", flush=True)

    try:

        response = await ask_groq(
            "Respond with exactly: Groq connection successful."
        )

        print("\nGroq response:", flush=True)
        print(response, flush=True)

        print("\nGroq connection test PASSED.", flush=True)

    except Exception as e:

        print("\nGroq connection test FAILED.", flush=True)
        print(f"Error type: {type(e).__name__}", flush=True)
        print(f"Error: {e}", flush=True)


if __name__ == "__main__":
    asyncio.run(main())