"""Entry point for syncing data with Notion.

The script intentionally keeps business logic minimal because different agents
will implement their own synchronization routines. What remains is the secure
credential loading pattern shared across the codebase.
"""
from __future__ import annotations

import logging
from pathlib import Path
from typing import Optional

from src.shared.notion_config import NotionSettings, load_notion_settings

logger = logging.getLogger(__name__)


def _describe_settings(settings: NotionSettings) -> str:
    """Build a safe, non-sensitive description for logging."""

    suffix = " with parent page" if settings.parent_page_id else ""
    return f"Notion database {settings.database_id}{suffix}"


def run_sync(*, config_path: Optional[str] = None) -> None:
    """Load Notion credentials and stub out sync logic.

    Parameters
    ----------
    config_path:
        Optional override path pointing at a custom Notion YAML configuration.
    """

    path_override = Path(config_path) if config_path else None
    settings = load_notion_settings(path_override)
    logger.info("Loaded %s configuration", _describe_settings(settings))
    # Real sync code would go here. We only demonstrate the secure config loader.


def main() -> None:
    logging.basicConfig(level=logging.INFO, format="%(levelname)s %(name)s: %(message)s")
    run_sync()


if __name__ == "__main__":
    main()
