"""
This package contains the Airflow AI SDK.
"""

from typing import Any

__version__ = "0.1.0a1"

from airflow_ai_sdk.decorators.agent import agent
from airflow_ai_sdk.decorators.branch import llm_branch
from airflow_ai_sdk.decorators.llm import llm
from airflow_ai_sdk.models.base import BaseModel

__all__ = ["agent", "llm", "llm_branch", "BaseModel"]


def get_provider_info() -> dict[str, Any]:
    return {
        "package-name": "airflow-ai-sdk-slim",
        "name": "Airflow AI SDK Slim",
        "description": "Slimmed down version of the Airflow AI SDK",
        "versions": [__version__],
        "task-decorators": [
            {
                "name": "agent",
                "class-name": "airflow_ai_sdk.decorators.agent.agent",
            },
            {
                "name": "llm",
                "class-name": "airflow_ai_sdk.decorators.llm.llm",
            },
            {
                "name": "llm_branch",
                "class-name": "airflow_ai_sdk.decorators.branch.llm_branch",
            },
        ],
    }
