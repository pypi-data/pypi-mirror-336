# Persona CLI

**Persona CLI** is a command-line tool for creating and managing projects that use the `persona-toolkit` — a modular
function-calling framework designed for agent-based systems.

This CLI helps you scaffold projects, generate tools, test them locally, and run the FastAPI server that exposes your
tools via REST API.

---

## 🚀 Installation

To use the CLI, first install the `persona-toolkit` library (assuming it's published or available locally):

```bash
pip install persona-toolkit
```

> Or if you're developing locally:

```bash
cd persona-toolkit/
poetry install
```

The CLI is exposed as:

```bash
persona-toolkit
```

---

## 📆 Features

### `init`

Create a new project scaffold with Poetry and the required structure:

```bash
persona-toolkit init my-project
```

This will:

- Initialize a Poetry project
- Install `persona-toolkit` as a dependency
- Create a `tools/` folder where your tools will live

---

### `add-tool`

Add a new tool interactively:

```bash
persona-toolkit add-tool
```

You'll be prompted for a tool name. A new Python file will be created in the `tools/` directory with a ready-to-edit
template including:

- `Input` and `Output` models (using Pydantic)
- A `run()` function

---

### `test-tool`

Test a tool locally by manually entering its input values:

```bash
persona-toolkit test-tool echo
```

This will:

- Import the specified tool from the `tools/` directory
- Prompt for input fields
- Run the `run()` function and show the output

You can use the cli to pass input values:

```bash
persona-toolkit test-tool echo --input '{"message": "Hello, World!"}'
```

---

### `run`

Start the FastAPI server and expose your tools via HTTP:

```bash
persona-toolkit run --port 8000
```

You can now access:

- `GET /tools` — list available tools
- `GET /tools/{tool}/schema` — get tool schema
- `POST /invocations` — run a tool

---

## 🗂 Project Structure

```bash
my-project/
├── pyproject.toml         # Poetry project config
├── tools/
│   └── echo_test.py            # Example tool
```

Each tool must define:

- `NAME` (a str with tool name)
- `Input` (a Pydantic model)
- `Output` (a Pydantic model)
- `run(input: Input, **kwargs) -> Output`

> kwargs includes: `project_id`, `session_id` and `user_id`

---

## 💡 Example Tool

```python
# tools/echo_test.py

from pydantic import BaseModel, Field

NAME = "echo"


class Input(BaseModel):
    message: str = Field(description="Message to echo")


class Output(BaseModel):
    message: str


def run(input: Input, **kwargs) -> Output:
    """Echo the message back"""
    return Output(message=f"Echo: {input.message}")
```

---

## ✅ Requirements

- Python 3.10+
- Poetry
- Uvicorn (installed automatically)

---

## 📃 License

MIT License

---

Built for the [Persona Agent System](https://github.com/your-org/persona) 🤖

