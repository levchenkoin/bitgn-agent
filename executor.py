from __future__ import annotations

from models import ToolCall, ToolResult


def execute_tool_call(tool_call: ToolCall) -> ToolResult:
    """
    Local stub executor.
    Later we will replace this with real BitGN API execution.
    """
    return ToolResult(
        tool_name=tool_call.tool_name,
        success=True,
        output={
            "message": f"Stub execution for tool '{tool_call.tool_name}'",
            "arguments": tool_call.arguments,
        },
    )