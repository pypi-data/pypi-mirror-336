import os
import sys
import json
from click import secho
from sktaip_cli.utils import LanggraphConfig, get_python_version
from sktaip_cli.exec import Runner, subp_exec
from sktaip_cli.progress import Progress
import tempfile


def generate_dockerfile(
    langgraph_config: LanggraphConfig, python_version: str = "3.12"
) -> str:
    include_paths = langgraph_config.get("include_path", [])
    graph_name = langgraph_config.get("graph_name", "external_graph")
    graph_path = langgraph_config.get("graph_path")
    env_file = langgraph_config.get("env_file")
    requirements_file = langgraph_config.get("requirements_file")

    dockerfile_additions = ""
    for include_paths in include_paths:
        dockerfile_additions += f"ADD {include_paths} /workdir/{include_paths}\n"
    dockerfile_content = f"""ARG PLATFORM_ARCH="linux/amd64"

FROM --platform=${{PLATFORM_ARCH}} python:{python_version}-bookworm

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
ENV PATH="/home/user/.local/bin:$PATH"
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
    return dockerfile_content


def dockerfile_build(
    directory: str, dockerfile: str, tag: str, docker_build_args: list[str]
):
    with Runner() as runner:
        with Progress(message="Building...") as set:
            build_cmd = [
                "docker",
                "build",
                directory,
                "-t",
                tag,
                "-f",
                dockerfile,
            ]
            if docker_build_args:
                build_cmd.extend(docker_build_args)
            runner.run(subp_exec(*build_cmd, verbose=True))
            secho(f"✅ Build completed", fg="green")
            secho(f"🐳 Image: {tag}", fg="green")


def create_dockerfile_and_build(
    base_image: str,
    tag: str,
    config: LanggraphConfig,
    docker_build_args: list[str],
    pull: bool,
    directory: str,
):
    with (
        Runner() as runner,
        Progress(message="Pulling...") as set,
    ):  # pull 옵션 처리: 베이스 이미지 최신버전 가져오기
        python_version = get_python_version()
        if pull:
            base_image = (
                base_image if base_image else "python:{python_version}-bookworm"
            )
            runner.run(
                subp_exec(
                    "docker",
                    "pull",
                    base_image,
                    verbose=True,
                )
            )
        set("Building...")

        secho(f"📝 Generating Dockerfile at temp directory", fg="yellow")
        dockerfile_content = generate_dockerfile(config, python_version)
        # 임시 Dockerfile 생성
        with tempfile.NamedTemporaryFile(
            mode="w", delete=False, suffix="tmpsktaip.Dockerfile"
        ) as tmp:
            dockerfile_path = tmp.name
            tmp.write(dockerfile_content)
            secho(
                f"📝 GeneratingTemporary Dockerfile at {dockerfile_path}",
                fg="yellow",
            )
        try:
            build_cmd = [
                "docker",
                "build",
                directory,
                "-t",
                tag,
                "-f",
                dockerfile_path,
            ]
            if docker_build_args:
                build_cmd.extend(docker_build_args)
            runner.run(subp_exec(*build_cmd, verbose=True))
            secho(f"✅ Build completed", fg="green")
            secho(f"🐳 Image: {tag}", fg="green")

        finally:
            os.remove(dockerfile_path)
            secho(f"✅ Temporary Dockerfile removed", fg="green")
