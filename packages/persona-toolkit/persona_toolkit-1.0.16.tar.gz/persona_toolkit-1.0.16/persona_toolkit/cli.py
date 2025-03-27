import asyncio
import json
import os
import subprocess
from pathlib import Path

import toml
import typer
from rich import print
from rich.prompt import Prompt
from typing_extensions import Optional, Annotated

app = typer.Typer(help="CLI for managing persona-toolkit projects")


@app.command()
def init(project_name: str):
    """
    Initialize a new persona-toolkit project using Poetry.
    """
    print(f"🚀 Creating project: [bold cyan]{project_name}[/bold cyan]")
    project_path = Path(project_name)
    project_path.mkdir(exist_ok=True)
    os.chdir(project_path)

    subprocess.run([
        "poetry", "init",
        "--name", project_name,
        "--dependency", "persona-toolkit",
        "--python", ">=3.10,<4.0",
        "--no-interaction"
    ], check=True)

    readme_content = """
# Persona Toolkit

This project was created using the persona-toolkit CLI.
"""

    Path("README.md").write_text(readme_content)
    Path(project_name).mkdir(exist_ok=True)
    (Path(project_name) / "__init__.py").touch()
    Path("tools").mkdir(exist_ok=True)

    # ✨ Update pyproject.toml to include CLI script
    pyproject_file = Path("pyproject.toml")
    data = toml.load(pyproject_file)

    data.setdefault("tool", {}).setdefault("poetry", {}).setdefault("scripts", {})[
        "persona-toolkit"
    ] = "persona_toolkit.cli:app"

    with open(pyproject_file, "w") as f:
        # noinspection PyTypeChecker
        toml.dump(data, f)

    subprocess.run(["poetry", "install"], check=True)

    print("✅ Project initialized.")
    print("➡️ You can now add tools using: [green]persona-toolkit add-tool[/green]")


@app.command()
def add_tool():
    """
    Create a new tool using an interactive wizard.
    """
    tool_name = Prompt.ask("🔧 Tool name (e.g. echo)")
    file_path = Path("tools") / f"{tool_name}.py"

    if file_path.exists():
        print(f"[red]⚠️ Tool '{tool_name}' already exists.")
        raise typer.Exit()

    template = f"""from pydantic import BaseModel, Field
    
NAME = "{tool_name}"

class Input(BaseModel):
    value: str = Field(description="Value to process")

class Output(BaseModel):
    result: str

def run(args: Input, **kwargs) -> Output:
    \"\"\"Example tool: {tool_name}\"\"\"
    return Output(result=f"Processed: {{input.value}}")
"""

    file_path.write_text(template)

    print(f"✅ Tool '{tool_name}' created at [green]{file_path}[/green]")


@app.command()
def test_tool(tool_name: str, args: Annotated[str, typer.Argument()] = None):
    """
    Manually test a tool locally by invoking it with input values.
    """
    import importlib

    params = json.loads(args) if args else {}

    print(f"🧪 Testing tool: [cyan]{tool_name}[/cyan]")
    print(f"🔹 Input: {params}")

    try:
        module = importlib.import_module(f"tools.{tool_name}")
        _input = module.Input
        _run = module.run

        print(f"🧪 Enter input for tool: [cyan]{tool_name}[/cyan]")
        fields = {}
        for name, field in _input.model_fields.items():
            if name in params:
                fields[name] = params[name]
                continue
            value = Prompt.ask(f"🔹 {name} ({field.annotation.__name__})")
            fields[name] = json.loads(value)

        input_obj = _input(**fields)

        if asyncio.iscoroutinefunction(_run):
            result = asyncio.run(_run(input_obj))
        else:
            result = _run(input_obj)

        print(f"✅ Output: [green]{result.model_dump()}[/green]")

    except ModuleNotFoundError:
        print(f"[red]❌ Tool '{tool_name}' not found.")
    except Exception as e:
        print(f"[red]💥 Error: {e}[/red]")


@app.command()
def run(port: int = typer.Option(8000, help="Port to run the server on")):
    """
    Start the FastAPI server on the specified port.
    """
    subprocess.run(
        [
            "poetry",
            "run",
            "uvicorn",
            "persona_toolkit.server:app",
            "--host", "0.0.0.0",
            "--port",
            str(port),
        ]
    )


if __name__ == "__main__":
    app()
