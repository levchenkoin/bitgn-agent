from agent import TrustworthyAgent
from client import load_demo_task
from config import settings


def main() -> None:
    task = load_demo_task()
    agent = TrustworthyAgent(
        max_steps=settings.max_steps,
        stagnation_limit=settings.stagnation_limit,
    )

    result, state = agent.run(task)

    print("\n=== TASK ===")
    print(task.instruction)

    print("\n=== TRACE ===")
    for note in state.notes:
        print(f"- {note}")

    if state.tool_history:
        print("\n=== TOOLS USED ===")
        for i, tool_call in enumerate(state.tool_history, start=1):
            print(f"{i}. {tool_call.tool_name} {tool_call.arguments}")

    if state.result_history:
        print("\n=== TOOL RESULTS ===")
        for i, tool_result in enumerate(state.result_history, start=1):
            print(f"{i}. success={tool_result.success}, tool={tool_result.tool_name}")
            print(f"   output={tool_result.output}")
            if tool_result.error:
                print(f"   error={tool_result.error}")

    if state.warnings:
        print("\n=== WARNINGS ===")
        for warning in state.warnings:
            print(f"- {warning}")

    print("\n=== FINAL RESULT ===")
    print(result)


if __name__ == "__main__":
    main()