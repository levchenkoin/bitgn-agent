from __future__ import annotations

from typing import Any, Literal
from pydantic import BaseModel, Field


class Task(BaseModel):
    task_id: str
    instruction: str
    context: dict[str, Any] = Field(default_factory=dict)
    available_tools: list[dict[str, Any]] = Field(default_factory=list)
    output_requirements: dict[str, Any] = Field(default_factory=dict)


class ToolCall(BaseModel):
    tool_name: str
    arguments: dict[str, Any] = Field(default_factory=dict)


class AgentDecision(BaseModel):
    thought_summary: str
    action_type: Literal["tool_call", "final_answer", "refuse"]
    tool_call: ToolCall | None = None
    final_answer: str | None = None
    confidence: float = 0.0


class ToolResult(BaseModel):
    tool_name: str
    success: bool
    output: Any = None
    error: str | None = None


class AgentState(BaseModel):
    step: int = 0
    completed: bool = False
    notes: list[str] = Field(default_factory=list)
    tool_history: list[ToolCall] = Field(default_factory=list)
    result_history: list[ToolResult] = Field(default_factory=list)
    warnings: list[str] = Field(default_factory=list)