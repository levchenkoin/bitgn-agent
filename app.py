from agent import TrustworthyAgent
from client import load_demo_task
from config import settings


def main() -> None:
    task = load_demo_task()
    agent = TrustworthyAgent(
        max_steps=settings.max_steps,
        stagnation_limit=settings.stagnation_limit,
    )
    result = agent.run(task)
    print("=== FINAL RESULT ===")
    print(result)


if __name__ == "__main__":
    main()