from __future__ import annotations

from pathlib import Path

from models import ToolCall, ToolResult


def execute_tool_call(tool_call: ToolCall) -> ToolResult:
    if tool_call.tool_name == "read_file":
        file_path = tool_call.arguments.get("path", "")

        if not file_path:
            return ToolResult(
                tool_name=tool_call.tool_name,
                success=False,
                error="Missing required argument: path",
            )

        path = Path(file_path)

        if not path.exists():
            return ToolResult(
                tool_name=tool_call.tool_name,
                success=False,
                error=f"File not found: {file_path}",
            )

        if not path.is_file():
            return ToolResult(
                tool_name=tool_call.tool_name,
                success=False,
                error=f"Path is not a file: {file_path}",
            )

        try:
            content = path.read_text(encoding="utf-8")
            return ToolResult(
                tool_name=tool_call.tool_name,
                success=True,
                output={
                    "path": file_path,
                    "content": content,
                },
            )
        except Exception as e:
            return ToolResult(
                tool_name=tool_call.tool_name,
                success=False,
                error=str(e),
            )

    return ToolResult(
        tool_name=tool_call.tool_name,
        success=False,
        error=f"Unsupported tool: {tool_call.tool_name}",
    )