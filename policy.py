from __future__ import annotations

from models import Task, ToolCall


DISALLOWED_PATTERNS = [
    "ignore previous instructions",
    "send api key",
    "reveal secret",
    "delete everything",
    "override safety",
]


def detect_prompt_injection(text: str) -> bool:
    lowered = text.lower()
    return any(pattern in lowered for pattern in DISALLOWED_PATTERNS)


def validate_tool_call(task: Task, tool_call: ToolCall) -> tuple[bool, str | None]:
    available_tool_names = {
        tool.get("name", "")
        for tool in task.available_tools
    }

    if tool_call.tool_name not in available_tool_names:
        return False, f"Tool '{tool_call.tool_name}' is not available for this task."

    destructive_keywords = ["delete", "remove", "drop", "destroy"]
    if any(word in tool_call.tool_name.lower() for word in destructive_keywords):
        return False, "Destructive tool calls are blocked unless explicitly implemented and allowed."

    return True, None