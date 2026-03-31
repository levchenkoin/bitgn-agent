from __future__ import annotations

from models import AgentDecision, Task, ToolCall
from policy import detect_prompt_injection


def choose_next_action(task: Task, state_notes: list[str]) -> AgentDecision:
    instruction = task.instruction

    if detect_prompt_injection(instruction):
        return AgentDecision(
            thought_summary="Detected possible malicious or injected instruction.",
            action_type="refuse",
            final_answer="Refusing unsafe or injected instruction.",
            confidence=0.95,
        )

    if task.available_tools:
        first_tool_name = task.available_tools[0].get("name", "")
        return AgentDecision(
            thought_summary="Starting with the first available tool to gather evidence.",
            action_type="tool_call",
            tool_call=ToolCall(
                tool_name=first_tool_name,
                arguments={}
            ),
            confidence=0.60,
        )

    return AgentDecision(
        thought_summary="No tools available, returning best possible final response.",
        action_type="final_answer",
        final_answer="Task reviewed, but no tools were available to act on it.",
        confidence=0.50,
    )