import sys
import click
import json
from typing import TypedDict
import os


class LanggraphConfig(TypedDict):
    include_path: list[str]
    graph_path: str
    env_file: str
    requirements_file: str
    graph_name: str | None


def validate_langgraph_json(langgraph_json: str) -> LanggraphConfig:
    with open(langgraph_json, "r") as f:
        config = json.load(f)

    required_fields = ["include_path", "graph_path", "env_file", "requirements_file"]
    missing_fields = [field for field in required_fields if not config.get(field)]
    if missing_fields:
        raise click.UsageError(
            f"Required fields missing in {langgraph_json}: {', '.join(missing_fields)}"
        )
    return LanggraphConfig(**config)


def get_python_version() -> str:
    if sys.version_info < (3, 10) or sys.version_info > (3, 12):
        py_version_msg = (
            "\n\nNote: The in-mem server requires Python 3.10 ~ 3.12."
            f" You are currently using Python {sys.version_info.major}.{sys.version_info.minor}."
            ' Please upgrade your Python version before installing "sktaip_api".'
        )
        raise click.UsageError(py_version_msg)

    return ".".join(map(str, sys.version_info[:2]))


def save_docker_credentials(username, password):
    """Docker 로그인 정보를 .docker_auth.json에 저장합니다."""
    credentials = {"username": username, "password": password}
    with open(".docker_auth.json", "w") as f:
        json.dump(credentials, f)


def load_docker_credentials():
    """저장된 Docker 로그인 정보를 로드합니다."""
    if not os.path.exists(".docker_auth.json"):
        raise FileNotFoundError("Docker credentials not found. Please login first.")

    with open(".docker_auth.json", "r") as f:
        credentials = json.load(f)
    return credentials.get("username"), credentials.get("password")
