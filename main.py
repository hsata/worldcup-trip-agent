import os
import asyncio
from dotenv import load_dotenv

load_dotenv()

os.environ["GOOGLE_GENAI_USE_VERTEXAI"] = os.getenv("GOOGLE_GENAI_USE_VERTEXAI", "TRUE")
os.environ["GOOGLE_CLOUD_PROJECT"] = os.getenv("GOOGLE_CLOUD_PROJECT", "")
os.environ["GOOGLE_CLOUD_LOCATION"] = os.getenv("GOOGLE_CLOUD_LOCATION", "us-central1")

from worldcup_agent.tracing_setup import setup_tracing
from worldcup_agent.agent import worldcup_agent
from worldcup_agent.evaluator import evaluate_response
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai.types import Content, Part

setup_tracing()

runner = Runner(
    agent=worldcup_agent,
    app_name="worldcup_tripmate",
    session_service=InMemorySessionService(),
)


async def chat():
    """Chat loop with automatic evaluation after each response."""
    session = await runner.session_service.create_session(
        app_name="worldcup_tripmate",
        user_id="test_user",
    )

    print("\nWorldCup TripMate — Type quit to exit\n")

    while True:
        user_input = input("You: ").strip()
        if user_input.lower() in ("quit", "exit", "q"):
            print("Goodbye!")
            break

        content = Content(parts=[Part(text=user_input)], role="user")

        response_text = ""
        async for event in runner.run_async(
            user_id="test_user",
            session_id=session.id,
            new_message=content,
        ):
            if event.content and event.content.parts:
                for part in event.content.parts:
                    if part.text:
                        response_text += part.text

        print(f"\nTripMate: {response_text}\n")

        # Auto-evaluate every response in background
        eval_result = await evaluate_response(user_input, response_text)
        if eval_result.get("scores"):
            scores = eval_result["scores"]
            print(f"  [Eval] Overall: {scores.get('overall', '?')}/5 | "
                  f"Weakest: {eval_result.get('weakest_area', '?')} | "
                  f"Tip: {eval_result.get('suggestion', '')[:80]}")
        print()


if __name__ == "__main__":
    asyncio.run(chat())
