import os
import sys
import click
import json
from click import secho
import pathlib
import shutil
from typing import Sequence, Optional
import tempfile
import subprocess
from sktaip_cli.docker import (
    generate_dockerfile,
    dockerfile_build,
    create_dockerfile_and_build,
)
from sktaip_cli.exec import Runner, subp_exec
from sktaip_cli.progress import Progress
from sktaip_cli.utils import (
    get_python_version,
    validate_langgraph_json,
    LanggraphConfig,
    save_docker_credentials,
    load_docker_credentials
)
from sktaip_cli.port import build_docker_image, docker_login




@click.group()
def cli():
    """Command-line interface for AIP server management."""
    pass

# 1. Docker Login
@cli.command()
@click.option("--username", prompt=True, help="Docker Hub username")
@click.option("--password", prompt=True, hide_input=True, help="Docker Hub password")
def login(username, password):
    """Docker Hub에 로그인하고 정보를 저장합니다."""
    docker_login(username, password)
    save_docker_credentials(username, password)


# 2. Run API Server on Local

@cli.command(help="🖥 Run the API server on local")
@click.option("--host", default="127.0.0.1", help="Host address")
@click.option("--port", default=28080, type=int, help="Port number")
@click.option(
    "--langgraph_json", default="./langgraph.json", help="Path to langgraph.json"
)
def dev(host, port, langgraph_json):
    """Run the development server."""
    try:
        from sktaip_api.server import run_server
    except ImportError as e:
        py_version_msg = ""
        if sys.version_info < (3, 10) or sys.version_info > (3, 12):
            py_version_msg = (
                "\n\nNote: The in-mem server requires Python 3.10 ~ 3.12."
                f" You are currently using Python {sys.version_info.major}.{sys.version_info.minor}."
                ' Please upgrade your Python version before installing "sktaip_api".'
            )
        try:
            from importlib import util

            if not util.find_spec("sktaip_api"):
                raise click.UsageError(
                    "Required package 'sktaip_api' is not installed.\n"
                    "Please install it with:\n\n"
                    '    pip install -U "sktaip_api"'
                    f"{py_version_msg}"
                )
        except ImportError:
            raise click.UsageError(
                "Could not verify package installation. Please ensure Python is up to date and\n"
                "Please install it with:\n\n"
                '    pip install -U "sktaip_api"'
                f"{py_version_msg}"
            )
        raise click.UsageError(
            "Could not import run_server. This likely means your installation is incomplete.\n"
            "Please install it with:\n\n"
            '    pip install -U "sktaip_api"'
            f"{py_version_msg}"
        )

    working_dir = os.getcwd()
    working_dir = os.path.abspath(working_dir)

    config_path = os.path.join(working_dir, langgraph_json)
    config: LanggraphConfig = validate_langgraph_json(config_path)

    # include_path를 Python 경로에 추가
    include_paths = config.get("include_path", [])
    for path in include_paths:
        # 상대 경로를 절대 경로로 변환
        abs_path = os.path.abspath(os.path.join(working_dir, path))
        if abs_path not in sys.path:
            sys.path.append(abs_path)
    graph_path = config.get("graph_path")
    abs_graph_path = os.path.abspath(os.path.join(working_dir, graph_path))
    env_path = config.get("env_file")
    abs_env_file = os.path.abspath(os.path.join(working_dir, env_path))

    secho(
        f"Starting server at {host}:{port}. Graph path: {abs_graph_path}",
        fg="green",
    )
    run_server(
        host=host,
        port=port,
        graph_name=config.get("graph_name") or "langgraph code",
        graph_path=abs_graph_path,
        reload=True,
        env_file=abs_env_file,
    )


@cli.command(help="🐳 Generate a Dockerfile for Agent API Server")
@click.option("--output", default="./sktaip.Dockerfile", help="Path to Dockerfile")
@click.option(
    "--langgraph_json", default="./langgraph.json", help="Path to langgraph.json"
)
def dockerfile(output: str, langgraph_json: str) -> None:
    """Dockerfile 내용을 생성합니다."""
    save_path = pathlib.Path(output).absolute()
    secho(f"🔍 Validating configuration at path: {langgraph_json}", fg="yellow")
    config: LanggraphConfig = validate_langgraph_json(langgraph_json)
    secho("✅ Configuration validated!", fg="green")
    secho(f"📝 Generating Dockerfile at {save_path}", fg="yellow")
    python_version = get_python_version()
    dockerfile_content = generate_dockerfile(config, python_version)
    with open(str(save_path), "w", encoding="utf-8") as f:
        f.write(dockerfile_content)
    secho("✅ Created: Dockerfile", fg="green")


@cli.command(help="🐳 Build a Docker image for Agent API Server")
@click.option(
    "--tag",
    "-t",
    help="""Tag for the docker image.

    \b
    Example:
        langgraph build -t my-image

    \b
    """,
    required=True,
)
@click.option(
    "--dockerfile",
    "-f",
    help="""File path to the Dockerfile. If not provided, a Dockerfile will be generated automatically.
    """,
    required=False,
    default=None,
)
@click.option(
    "--base-image",
    hidden=True,
)
@click.option(
    "--langgraph_json", default="./langgraph.json", help="Path to langgraph.json"
)
@click.option("--pull", is_flag=True, help="Pull the latest base image")
@click.option("--directory", "-d", help="Directory to build the image", default=".")
@click.argument("docker_build_args", nargs=-1, type=click.UNPROCESSED)
def build(
    langgraph_json: str,
    docker_build_args: Sequence[str],
    base_image: Optional[str],
    tag: str,
    pull: bool,
    directory: str,
    dockerfile: Optional[str],
):
    # Docker 설치 확인
    if shutil.which("docker") is None:
        raise click.ClickException("Docker가 설치되어 있지 않습니다.")

    secho(f"🔍 Validating configuration at path: {langgraph_json}", fg="yellow")
    config: LanggraphConfig = validate_langgraph_json(langgraph_json)
    secho("✅ Configuration validated!", fg="green")
    if dockerfile:
        secho(f"📝 Using Dockerfile at {dockerfile}", fg="yellow")
        dockerfile_build(directory, dockerfile, tag, docker_build_args)
    else:
        create_dockerfile_and_build(base_image, tag, config, docker_build_args, pull, directory)


@cli.command()
@click.option("--app-id", required=True, help="Application ID")
def create_apikey(app_id):
    """API 키를 생성합니다."""
    try:
        subprocess.run(["sktaip-cli", "create-apikey", "--app_id", app_id], check=True)
        click.secho(f"Successfully created API key for {app_id}", fg="green")
    except subprocess.CalledProcessError:
        click.secho(f"Failed to create API key for {app_id}", fg="red")


# 5. sktaip-cli get-apikey
@cli.command()
@click.option("--app-id", required=True, help="Application ID")
def get_apikey(app_id):
    """API 키를 가져옵니다."""
    try:
        subprocess.run(["sktaip-cli", "get-apikey", "--app_id", app_id], check=True)
        click.secho(f"Successfully retrieved API key for {app_id}", fg="green")
    except subprocess.CalledProcessError:
        click.secho(f"Failed to retrieve API key for {app_id}", fg="red")


# 6. sktaip-cli invoke-example
@cli.command()
def invoke_example():
    """예제 API 호출"""
    try:
        subprocess.run(["sktaip-cli", "invoke-example"], check=True)
        click.secho("Successfully invoked the example API.", fg="green")
    except subprocess.CalledProcessError:
        click.secho("Failed to invoke the example API.", fg="red")

if __name__ == "__main__":
    cli()
