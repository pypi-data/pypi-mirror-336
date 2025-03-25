import subprocess
import click

import json
import click
import subprocess


# Dockerfile 생성
def generate_dockerfile(output: str, langgraph_json: str):
    """Dockerfile을 생성합니다."""
    config = json.load(open(langgraph_json))
    include_paths = config.get("include_path", [])
    graph_name = config.get("graph_name", "external_graph")
    graph_path = config.get("graph_path")
    env_file = config.get("env_file")
    requirements_file = config.get("requirements_file")
    
    required_configs = ["include_path", "graph_path", "env_file", "requirements_file"]
    for config_item in required_configs:
        if config_item not in config:
            raise click.UsageError(
                f"Required config {config_item} is not set in {langgraph_json}"
            )

    dockerfile_additions = ""
    for path in include_paths:
        dockerfile_additions += f"ADD {path} /workdir/{path}\n"

    dockerfile_content = f"""
ARG PLATFORM_ARCH="linux/amd64"

FROM --platform=${{PLATFORM_ARCH}} python:3.12-bookworm

ENV LANG=C.UTF-8 LC_ALL=C.UTF-8 
ENV PYTHONUNBUFFERED=1

RUN apt-get update && \\
    apt-get install -y vim curl yq jq
RUN addgroup -gid 1000 usergroup && \\
    adduser user \\
    --disabled-password \\
    -u 1000 --gecos "" \\
    --ingroup 0 \\
    --ingroup usergroup && \\
    mkdir -p /workdir && \\
    chown -R user:usergroup /workdir

WORKDIR /workdir

ENV PATH="${{HOME}}/.local/bin:${{PATH}}"
ENV ENV_FILE="{env_file}"
USER user

ENV GRAPH_PATH="{graph_path}"
ENV APP_NAME="{graph_name}"
ENV REQUIREMENTS_FILE="{requirements_file}"
ENV WORKER_CLASS="uvicorn.workers.UvicornWorker"

ENV APP__HOST=0.0.0.0
ENV APP__PORT=28080
ENV LOG_LEVEL=info
ENV GRACEFUL_TIMEOUT=600
ENV TIMEOUT=600
ENV KEEP_ALIVE=600

# For distinguishing between deployed app and agent-backend
ENV IS_DEPLOYED_APP=true

{dockerfile_additions}

ADD . /workdir
RUN python -m pip install sktaip-cli
RUN python -m pip install -r ${{REQUIREMENTS_FILE}}

RUN echo 'import os' > /workdir/server.py && \\
    echo 'from sktaip_api.server import create_app, load_environment' >> /workdir/server.py && \\
    echo '' >> /workdir/server.py && \\
    echo 'env_file = os.getenv("ENV_FILE")' >> /workdir/server.py && \\
    echo 'load_environment(env_file)' >> /workdir/server.py && \\
    echo '' >> /workdir/server.py && \\
    echo 'graph_path = os.getenv("GRAPH_PATH")' >> /workdir/server.py && \\
    echo 'if graph_path is None:' >> /workdir/server.py && \\
    echo '    raise ValueError("GRAPH_PATH is not set")' >> /workdir/server.py && \\
    echo '' >> /workdir/server.py && \\
    echo 'app = create_app(graph_path)' >> /workdir/server.py

ENV APP_MODULE="server:app"
EXPOSE 28080
CMD python -m gunicorn \\
    -k "${{WORKER_CLASS}}" \\
    -b "${{APP__HOST}}:${{APP__PORT}}" \\
    --log-level "${{LOG_LEVEL}}" \\
    --graceful-timeout "${{GRACEFUL_TIMEOUT}}" \\
    --timeout "${{TIMEOUT}}" \\
    --keep-alive "${{KEEP_ALIVE}}" \\
    --preload "${{APP_MODULE}}"
"""
    
    with open(output, "w") as file:
        file.write(dockerfile_content)
    
    click.secho(f"Dockerfile has been generated at: {output}", fg="green")
    
# Docker 이미지 빌드
def build_docker_image(image_tag, dockerfile_path="./Dockerfile"):
    """Docker 이미지를 빌드합니다."""
    try:
        cmd = [
            "docker",
            "build",
            "-t", image_tag,
            "-f", dockerfile_path,
            "."
        ]
        subprocess.run(cmd, check=True)
        click.secho(f"Docker image '{image_tag}' has been successfully built.", fg="green")
    except subprocess.CalledProcessError as e:
        click.secho(f"Failed to build Docker image: {str(e)}", fg="red")
        raise click.UsageError("Docker build failed.")


def docker_login(username, password):
    """Docker Hub에 로그인합니다."""
    try:
        cmd = ["docker", "login", "-u", username, "-p", password]
        subprocess.run(cmd, check=True)
        click.secho("Docker login successful", fg="green")
    except subprocess.CalledProcessError:
        click.secho("Docker login failed. Please check your credentials.", fg="red")
        raise click.UsageError("Docker login failed.")
