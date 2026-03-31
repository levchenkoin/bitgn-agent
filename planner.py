import json

from llm import ask_llm
from models import AgentDecision, Task, ToolCall


def build_prompt(task: Task, state_notes: list[str]) -> str:
    return f"""
You are a trustworthy autonomous agent.

Task instruction:
{task.instruction}

Task context:
{task.context}

Available tools:
{task.available_tools}

Previous notes:
{state_notes}

Decide the single best next action.

Rules:
1. Only use tools from available_tools
2. Never invent tool names
3. Prefer safe, reversible actions
4. If the task is unsafe, refuse
5. If enough information is already available in Previous notes, provide final_answer
6. If file content has already been read, do not call the same read_file tool again unless needed
7. When using read_file, provide the file path in arguments as {{"path": "..."}}
8. Return ONLY valid JSON

JSON schema:
{{
  "thought_summary": "short explanation",
  "action_type": "tool_call" | "final_answer" | "refuse",
  "tool_name": "tool name or empty string",
  "arguments": {{}},
  "final_answer": "answer text or empty string",
  "confidence": 0.0
}}
""".strip()


def choose_next_action(task: Task, state_notes: list[str]) -> AgentDecision:
    prompt = build_prompt(task, state_notes)
    raw = ask_llm(prompt)

    try:
        data = safe_json_loads(raw)

        tool_call = None
        if data.get("action_type") == "tool_call":
            tool_call = ToolCall(
                tool_name=data.get("tool_name", ""),
                arguments=data.get("arguments", {}),
            )

        return AgentDecision(
            thought_summary=data.get("thought_summary", ""),
            action_type=data.get("action_type", "refuse"),
            tool_call=tool_call,
            final_answer=data.get("final_answer"),
            confidence=float(data.get("confidence", 0.0)),
        )
    except Exception as e:
        return AgentDecision(
            thought_summary=f"Failed to parse model output: {e}",
            action_type="refuse",
            final_answer="Model returned invalid JSON.",
            confidence=0.0,
        )

def safe_json_loads(raw: str) -> dict:
    raw = raw.strip()

    # Sometimes model can return ```json ... ```
    if raw.startswith("```"):
        raw = raw.strip("`")
        raw = raw.replace("json", "", 1).strip()

    # Try to find JSON inside the text
    start = raw.find("{")
    end = raw.rfind("}")

    if start != -1 and end != -1:
        raw = raw[start:end + 1]

    return json.loads(raw)