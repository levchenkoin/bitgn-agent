# BitGN Agent (MVP)

A minimal trustworthy AI agent built for the BitGN PAC challenge.

## Overview

This project implements a simple autonomous agent with:

* decision-making via LLM
* tool usage (`read_file`)
* state tracking (history of steps, tool calls, results)
* basic safety checks (tool validation, prompt injection patterns)

The agent follows a simple loop:
**plan → act → observe → respond**

## Features

* LLM-based planner
* Tool execution layer
* Agent state (notes, tool history, results)
* Safe tool validation
* Structured JSON decision-making
* Debug trace output

## Example Task

The agent can:

1. Read a file
2. Extract information
3. Produce a summary

## Project Structure

* `agent.py` — main agent loop
* `planner.py` — decision-making logic
* `executor.py` — tool execution
* `policy.py` — safety checks
* `models.py` — data models
* `client.py` — demo task
* `llm.py` — LLM integration
* `app.py` — entry point

## Setup

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
pip install openai
```

Create `.env`:

```env
OPENAI_API_KEY=your_key_here
MODEL_NAME=gpt-4.1-mini
```

## Run

```bash
python app.py
```

## Notes

This is an MVP version built for experimentation and learning.
Future improvements may include:

* multiple tools
* better memory handling
* BitGN API integration
* structured logging
