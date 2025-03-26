"""
This module provides functionalities to generate and manage Blaxel deployment configurations.
It includes functions to set default deployment values, create deployment configurations from resources,
format deployments, and clean up auto-generated deployments.
"""

import ast
import json
import os
import shutil
import sys
from logging import getLogger
from pathlib import Path
from typing import Literal

import yaml

from blaxel.api.agents import get_agent
from blaxel.authentication import new_client
from blaxel.client import AuthenticatedClient
from blaxel.common import slugify
from blaxel.common.settings import Settings, get_settings, init
from blaxel.models import (
    Agent,
    AgentSpec,
    Flavor,
    Function,
    FunctionKit,
    FunctionSpec,
    Metadata,
    MetadataLabels,
)

from .format import arg_to_dict
from .parser import Resource, get_description, get_resources, get_schema

sys.path.insert(0, os.getcwd())
sys.path.insert(0, os.path.join(os.getcwd(), "src"))

def handle_function_kit(deployment: Function):
    """
    Handles the function kit for a deployment.
    """
    settings = get_settings()
    deployment.spec.kit = []
    functions_kits = get_resources("kit", settings.server.directory)
    for function_kit in functions_kits:
        for arg in function_kit.decorator.keywords:
            if arg.arg == "parent" and isinstance(arg.value, ast.Constant) and slugify(arg.value.value) == deployment.metadata.name:
                kit = get_blaxel_deployment_from_resource(settings, function_kit)
                deployment.spec.kit.append(kit)
    return deployment


def set_default_values(resource: Resource, deployment: Agent | Function):
    """
    Sets default values for a deployment based on the resource and deployment type.

    Parameters:
        resource (Resource): The resource information.
        deployment (Agent | Function): The deployment instance to set defaults for.

    Returns:
        Agent | Function: The updated deployment with default values set.
    """
    settings = get_settings()
    deployment.metadata.workspace = settings.workspace
    if not deployment.metadata.name:
        deployment.metadata.name = slugify(resource.name)
    if not deployment.metadata.display_name:
        deployment.metadata.display_name = deployment.metadata.name
    if not deployment.spec.description:
        deployment.spec.description = get_description(None, resource)
    if isinstance(deployment, Function):
        for arg in resource.decorator.keywords:
            if arg.arg == "kit" and isinstance(arg.value, ast.Constant) and arg.value.value == True:
                deployment = handle_function_kit(deployment)
    if isinstance(deployment, Agent):
        deployment.spec.functions = []
        for arg in resource.decorator.keywords:
            if arg.arg == "remote_functions":
                if isinstance(arg.value, ast.List):
                    for value in arg.value.elts:
                        if isinstance(value, ast.Constant):
                            deployment.spec.functions.append(slugify(value.value))
    return deployment

def get_blaxel_deployment_from_resource(
    settings: Settings,
    resource: Resource,
) -> Agent | Function | FunctionKit:
    """
    Creates a deployment configuration from a given resource.

    Args:
        resource (Resource): The resource to create a deployment for.

    Returns:
        Agent | Function: The deployment configuration.
    """
    for arg in resource.decorator.keywords:
        if arg.arg == "agent":
            if isinstance(arg.value, ast.Dict):
                value = arg_to_dict(arg.value)
                metadata = Metadata(**value.get("metadata", {}))
                spec = AgentSpec(**value.get("spec", {}))
                agent = Agent(metadata=metadata, spec=spec)
                if not agent.spec.prompt:
                    agent.spec.prompt = get_description(None, resource)
                return set_default_values(resource, agent)
        if arg.arg == "function":
            if isinstance(arg.value, ast.Dict):
                value = arg_to_dict(arg.value)
                metadata = Metadata(**value.get("metadata", {}))
                spec = FunctionSpec(**value.get("spec", {}))
                func = Function(metadata=metadata, spec=spec)
                if not func.spec.schema:
                    func.spec.schema = get_schema(resource)
                return set_default_values(resource, func)
        if arg.arg == "kit":
            if isinstance(arg.value, ast.Dict):
                value = arg_to_dict(arg.value)
                kit = FunctionKit(**value)
                if not kit.description:
                    kit.description = get_description(None, resource)
                if not kit.schema:
                    kit.schema = get_schema(resource)
                return kit

    if resource.type == "agent":
        agent = Agent(metadata=Metadata(), spec=AgentSpec())
        return set_default_values(resource, agent)
    if resource.type == "function":
        func = Function(metadata=Metadata(), spec=FunctionSpec())
        func.spec.schema = get_schema(resource)
        return set_default_values(resource, func)
    if resource.type == "kit":
        kit = FunctionKit(
            name=slugify(resource.name),
            description=get_description(None, resource),
            schema=get_schema(resource)
        )
        return kit
    return None

def get_flavors(flavors: list[Flavor]) -> str:
    """
    Converts a list of Flavor objects to a JSON string.

    Args:
        flavors (list[Flavor]): List of Flavor objects.

    Returns:
        str: JSON string representation of flavors.
    """
    if not flavors:
        return "[]"
    return json.dumps([flavor.to_dict() for flavor in flavors])

def get_agent_yaml(
    agent: Agent, functions: list[tuple[Resource, Function]], settings: Settings, client: AuthenticatedClient
) -> str:
    """
    Generates YAML configuration for an agent deployment.

    Args:
        agent (Agent): Agent deployment configuration
        functions (list[tuple[Resource, FunctionDeployment]]): List of associated functions
        settings (Settings): Application settings

    Returns:
        str: YAML configuration string
    """
    try:
        agent_response = get_agent.sync(agent.metadata.name, client=client)
        agent.spec.repository = agent_response.spec.repository
    except Exception:
        pass
    agent.spec.functions = agent.spec.functions or []
    agent.spec.functions = agent.spec.functions + [slugify(function.metadata.name) for (_, function) in functions]
    agent.metadata.labels = agent.metadata.labels and MetadataLabels.from_dict(agent.metadata.labels) or MetadataLabels()
    agent.metadata.labels["x-blaxel-auto-generated"] = "true"
    agent_yaml = yaml.dump(agent.to_dict())
    template = f"""
apiVersion: blaxel.ai/v1alpha1
kind: Agent
{agent_yaml}
"""
    return template


def get_function_yaml(function: Function, settings: Settings, client: AuthenticatedClient) -> str:
    """
    Generates YAML configuration for a function deployment.

    Args:
        function (FunctionDeployment): Function deployment configuration
        settings (Settings): Application settings

    Returns:
        str: YAML configuration string
    """
    function.metadata.labels = function.metadata.labels and MetadataLabels.from_dict(function.metadata.labels) or MetadataLabels()
    function.metadata.labels["x-blaxel-auto-generated"] = "true"
    function_yaml = yaml.dump(function.to_dict())
    return f"""
apiVersion: blaxel.ai/v1alpha1
kind: Function
{function_yaml}
"""


def dockerfile(
    type: Literal["agent", "function"],
    resource: Resource,
    deployment: Agent | Function,
) -> str:
    """
    Generates Dockerfile content for agent or function deployment.

    Args:
        type (Literal["agent", "function"]): Type of deployment
        resource (Resource): Resource to be deployed
        deployment (Agent | Function): Resource configuration

    Returns:
        str: Dockerfile content
    """

    cliInstallUrl = "https://raw.githubusercontent.com/beamlit/toolkit/main/install.sh"
    # if os.getenv("BL_ENV") == "dev":
    #     cliInstallUrl = "https://raw.githubusercontent.com/cploujoux/toolkit/main/install.sh"

    settings = get_settings()
    if type == "agent":
        module = f"{resource.module.__file__.split('/')[-1].replace('.py', '')}.{resource.module.__name__}"
    else:
        module = f"functions.{resource.module.__file__.split('/')[-1].replace('.py', '')}.{resource.module.__name__}"
    cmd = ["bl", "serve", "--port", "80", "--module", module]
    if type == "agent":
        cmd.append("--remote")
    cmd_str = ",".join([f'"{c}"' for c in cmd])
    return f"""
FROM python:3.12-slim

ARG UV_VERSION="latest"
RUN apt update && apt install -y curl build-essential

# Install uv.
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/
RUN curl -fsSL {cliInstallUrl} | BINDIR=/bin sh
WORKDIR /blaxel

# Install the application dependencies.
COPY pyproject.toml /blaxel/pyproject.toml
COPY uv.lock /blaxel/uv.lock

COPY README.m[d] /blaxel/README.md
COPY LICENS[E] /blaxel/LICENSE
COPY {settings.server.directory} /blaxel/src

RUN uv sync --no-cache --no-dev

ENV PATH="/blaxel/.venv/bin:$PATH"

ENTRYPOINT [{cmd_str}]
"""

def clean_auto_generated(
    directory: str,
    type: Literal["agent", "function"],
    deployments: list[tuple[Resource, Agent | Function]]
):
    """
    Cleans up auto-generated deployments of a specific type.

    Args:
        directory (str): Base directory containing deployments.
        type (Literal["agent", "function"]): Type of deployment to clean ("agent" or "function").
        deployments (list[tuple[Resource, Agent | Function]]): List of deployment resources and configurations.
    """

    deploy_dir = Path(directory) / f"{type}s"
    deploy_names = [d.metadata.name for (_, d) in deployments]

    if deploy_dir.exists():
        for item_dir in deploy_dir.iterdir():
            if item_dir.is_dir() and item_dir.name not in deploy_names:
                yaml_file = item_dir / f"{type}.yaml"
                if yaml_file.exists():
                    with open(yaml_file) as f:
                        try:
                            content = yaml.safe_load(f)
                            if content.get("metadata", {}).get("labels", {}).get("x-blaxel-auto-generated") == "true":
                                shutil.rmtree(item_dir)
                        except yaml.YAMLError:
                            continue

def generate_blaxel_deployment(directory: str, name: str):
    """
    Generates all necessary deployment files for Blaxel agents and functions.

    Args:
        directory (str): Target directory for generated files.
        name (str): Name identifier for the deployment.

    Creates:
        - Agent and function YAML configurations.
        - Dockerfiles for each deployment.
        - Directory structure for agents and functions.
    """
    settings = init()
    client = new_client()
    logger = getLogger(__name__)
    logger.info(f"Importing server module: {settings.server.module}")
    functions: list[tuple[Resource, Function]] = []
    agents: list[tuple[Resource, Agent]] = []
    for resource in get_resources("agent", settings.server.directory):
        agent = get_blaxel_deployment_from_resource(settings, resource)
        if name and agent.metadata.name != name:
            agent.metadata.name = slugify(name)
        if agent:
            agents.append((resource, agent))
    for resource in get_resources("function", settings.server.directory):
        function = get_blaxel_deployment_from_resource(settings, resource)
        if function:
            functions.append((resource, function))

    agents_dir = os.path.join(directory, "agents")
    functions_dir = os.path.join(directory, "functions")
    # Create directory if it doesn't exist
    os.makedirs(agents_dir, exist_ok=True)
    os.makedirs(functions_dir, exist_ok=True)
    for resource, agent in agents:
        # write deployment file
        agent_dir = os.path.join(agents_dir, agent.metadata.name)
        os.makedirs(agent_dir, exist_ok=True)
        with open(os.path.join(agent_dir, "agent.yaml"), "w") as f:
            content = get_agent_yaml(agent, functions, settings, client)
            f.write(content)
        # write dockerfile for build
        with open(os.path.join(agent_dir, "Dockerfile"), "w") as f:
            content = dockerfile("agent", resource, agent)
            f.write(content)
    for resource, function in functions:
        # write deployment file
        function_dir = os.path.join(functions_dir, function.metadata.name)
        os.makedirs(function_dir, exist_ok=True)
        with open(os.path.join(function_dir, "function.yaml"), "w") as f:
            content = get_function_yaml(function, settings, client)
            f.write(content)
        # write dockerfile for build
        with open(os.path.join(function_dir, "Dockerfile"), "w") as f:
            content = dockerfile("function", resource, function)
            f.write(content)

    clean_auto_generated(directory, "agent", agents)
    clean_auto_generated(directory, "function", functions)