from __future__ import annotations

from models import Task


def load_demo_task() -> Task:
    return Task(
        task_id="demo-1",
        instruction="Read the file named notes.txt and summarize its content.",
        context={
            "source": "local_demo",
            "files": [
                {
                    "name": "notes.txt",
                    "path": "notes.txt",
                    "description": "A demo text file for the agent to read"
                }
            ]
        },
        available_tools=[
            {
                "name": "read_file",
                "description": "Read a file safely"
            },
        ],
        output_requirements={
            "must_include_references": False,
        },
    )