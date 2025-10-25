"""Helpers for loading Notion credentials without hard-coding secret names.

The loader reads the environment variable names from ``config/notion.yml`` so
that Terraform Cloud can inject the real credentials at runtime. This avoids
committing secret identifiers or values into the repository while keeping the
Python modules decoupled from the CI/CD secret naming convention.
"""
from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, Optional, Union
import os

import yaml


@dataclass(frozen=True)
class NotionSettings:
    """Concrete Notion credentials resolved from environment variables."""

    token: str
    database_id: str
    parent_page_id: Optional[str] = None


def _default_config_path() -> Path:
    """Return the repository-relative path for the Notion YAML config."""

    return Path(__file__).resolve().parents[2] / "config" / "notion.yml"


def load_notion_config(config_path: Optional[Union[Path, str]] = None) -> Dict[str, Any]:
    """Load the raw Notion configuration dictionary from YAML.

    Parameters
    ----------
    config_path:
        Optional override path for the YAML file. When ``None`` the helper uses
        the repository default (``config/notion.yml``).
    """

    path = Path(config_path) if config_path else _default_config_path()
    if not path.exists():
        raise FileNotFoundError(f"Notion config file not found at {path}")

    with path.open("r", encoding="utf-8") as handle:
        data = yaml.safe_load(handle) or {}

    if "notion" not in data:
        raise KeyError("The Notion config file must contain a 'notion' section.")

    return data["notion"]


def _require_env(name: str) -> str:
    """Fetch an environment variable or raise a clear error."""

    value = os.getenv(name)
    if value is None or value == "":
        raise EnvironmentError(
            f"Environment variable '{name}' is required for the Notion integration."
        )
    return value


def load_notion_settings(
    config_path: Optional[Union[Path, str]] = None,
) -> NotionSettings:
    """Resolve Notion credentials based on the shared YAML config."""

    config = load_notion_config(config_path)

    token = _require_env(config.get("token_env", "NOTION_TOKEN"))
    database_id = _require_env(config.get("database_id_env", "NOTION_DATABASE_ID"))

    parent_var = config.get("parent_page_id_env")
    parent_page_id = os.getenv(parent_var) if parent_var else None

    return NotionSettings(
        token=token,
        database_id=database_id,
        parent_page_id=parent_page_id,
    )


__all__ = ["NotionSettings", "load_notion_settings", "load_notion_config"]
