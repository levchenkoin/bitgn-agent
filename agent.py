from models import AgentState, Task
from executor import execute_tool_call
from planner import choose_next_action
from policy import validate_tool_call


class TrustworthyAgent:
    def __init__(self, max_steps: int = 12, stagnation_limit: int = 3) -> None:
        self.max_steps = max_steps
        self.stagnation_limit = stagnation_limit

    def run(self, task: Task) -> tuple[str, AgentState]:
        state = AgentState()
        repeated_no_progress = 0
        last_action_signature = None

        while not state.completed and state.step < self.max_steps:
            state.step += 1

            decision = choose_next_action(task, state.notes)
            state.notes.append(f"Step {state.step}: {decision.thought_summary}")

            if decision.action_type == "refuse":
                state.completed = True
                return decision.final_answer or "Refused for safety reasons.", state

            if decision.action_type == "final_answer":
                state.completed = True
                return decision.final_answer or "Completed.", state

            if decision.action_type == "tool_call" and decision.tool_call is not None:
                is_valid, error = validate_tool_call(task, decision.tool_call)
                if not is_valid:
                    state.warnings.append(error or "Unknown validation error")
                    state.completed = True
                    return f"Stopped: {error}", state

                current_signature = (
                    decision.tool_call.tool_name,
                    tuple(sorted(decision.tool_call.arguments.items()))
                )

                if current_signature == last_action_signature:
                    repeated_no_progress += 1
                else:
                    repeated_no_progress = 0

                last_action_signature = current_signature

                if repeated_no_progress >= self.stagnation_limit:
                    state.completed = True
                    return "Stopped early due to repeated non-progressing actions.", state

                result = execute_tool_call(decision.tool_call)
                state.tool_history.append(decision.tool_call)
                state.result_history.append(result)

                if result.success:
                    state.notes.append(
                        f"Tool {result.tool_name} succeeded with output: {result.output}"
                    )
                else:
                    state.warnings.append(result.error or "Tool execution failed")
                    state.notes.append(
                        f"Tool {result.tool_name} failed: {result.error or 'unknown error'}"
                    )

        return "Stopped: max steps reached.", state