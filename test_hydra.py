import asyncio

from app.llm.hydra_client import ask_hydra


async def main():
    print("Testing Hydra connection...")

    try:
        response = await ask_hydra(
            "Respond with exactly: Hydra connection successful."
        )

        print("\nHydra response:")
        print(response)

        print("\nHydra connection test PASSED.")

    except Exception as e:
        print("\nHydra connection test FAILED.")
        print(f"Error: {e}")


if __name__ == "__main__":
    asyncio.run(main())