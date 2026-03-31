from __future__ import annotations

from models import Task


def load_demo_task() -> Task:
    return Task(
        task_id="demo-1",
        instruction="Read the task and use available tools safely.",
        context={"source": "local_demo"},
        available_tools=[
            {"name": "read_file", "description": "Read a file safely"},
        ],
        output_requirements={
            "must_include_references": False,
        },
    )