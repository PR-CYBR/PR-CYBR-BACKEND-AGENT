#!/usr/bin/env python3
"""Synchronize GitHub events with Notion databases.

This module parses the GitHub event payload provided to GitHub Actions via
``GITHUB_EVENT_PATH`` and forwards the payload to the correct Notion handler.
Each handler is responsible for ensuring the matching Notion page exists and is
kept in sync with the GitHub resource.
"""
from __future__ import annotations

import json
import logging
import os
import sys
from dataclasses import dataclass
from typing import Any, Dict, Iterable, Optional

import requests
from notion_client import Client


LOGGER = logging.getLogger("notion-sync")


def configure_logging() -> None:
    """Configure structured logging for the script."""
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s %(levelname)s %(name)s %(message)s",
    )


def log(level: int, message: str, **context: Any) -> None:
    """Log a message with structured JSON context."""
    if context:
        message = f"{message} | {json.dumps(context, sort_keys=True)}"
    LOGGER.log(level, message)


class NotionClient:
    """Wrapper around the official Notion SDK with helper utilities."""

    def __init__(self, token: str) -> None:
        self._client = Client(auth=token)

    def find_page_by_github_id(self, database_id: str, github_id: str) -> Optional[Dict[str, Any]]:
        log(logging.DEBUG, "Searching for Notion page by GitHub ID", database_id=database_id, github_id=github_id)
        response = self._client.databases.query(
            **{
                "database_id": database_id,
                "filter": {
                    "property": "GitHub ID",
                    "rich_text": {"equals": github_id},
                },
            }
        )
        results = response.get("results", [])
        return results[0] if results else None

    def upsert_page(self, database_id: str, properties: Dict[str, Any], github_id: str) -> str:
        existing_page = self.find_page_by_github_id(database_id, github_id)
        if existing_page:
            page_id = existing_page["id"]
            log(logging.INFO, "Updating existing Notion page", page_id=page_id, github_id=github_id)
            self._client.pages.update(page_id=page_id, properties=properties)
            return page_id

        log(logging.INFO, "Creating new Notion page", database_id=database_id, github_id=github_id)
        new_page = self._client.pages.create(
            parent={"database_id": database_id},
            properties=properties,
        )
        return new_page["id"]


@dataclass
class GitHubNotifier:
    token: Optional[str]

    def headers(self) -> Dict[str, str]:
        if not self.token:
            return {}
        return {
            "Authorization": f"token {self.token}",
            "Accept": "application/vnd.github+json",
            "User-Agent": "pr-cybr-notion-sync-script",
        }

    def ensure_comment(self, comments_url: str, notion_page_id: str) -> None:
        """Ensure a comment referencing the Notion page exists for the resource."""
        if not self.token:
            log(logging.INFO, "Skipping GitHub comment because token is unavailable")
            return

        identifier = f"Notion Page ID: {notion_page_id}"
        try:
            response = requests.get(comments_url, headers=self.headers(), timeout=15)
            response.raise_for_status()
        except requests.RequestException as exc:
            log(logging.WARNING, "Failed to fetch existing comments", error=str(exc), comments_url=comments_url)
            return

        for comment in response.json():
            body = comment.get("body", "")
            if identifier in body:
                log(logging.DEBUG, "GitHub comment already references Notion page", notion_page_id=notion_page_id)
                return

        body = f"Automated sync: this GitHub item is linked to Notion page `{notion_page_id}`."
        try:
            response = requests.post(comments_url, headers=self.headers(), json={"body": body}, timeout=15)
            response.raise_for_status()
            log(logging.INFO, "Published GitHub comment linking to Notion page", comments_url=comments_url)
        except requests.RequestException as exc:
            log(logging.WARNING, "Failed to publish GitHub comment", error=str(exc), comments_url=comments_url)


class BaseSync:
    def __init__(self, notion: NotionClient, notifier: GitHubNotifier, database_id: str, payload: Dict[str, Any]):
        self.notion = notion
        self.notifier = notifier
        self.database_id = database_id
        self.payload = payload

    def sync(self) -> None:
        raise NotImplementedError

    @staticmethod
    def _truncate(content: str, limit: int = 2000) -> str:
        if len(content) <= limit:
            return content
        return f"{content[: limit - 1]}\u2026"

    @staticmethod
    def _text_property(content: str) -> Dict[str, Any]:
        safe_content = BaseSync._truncate(content)
        return {"rich_text": [{"type": "text", "text": {"content": safe_content}}]}

    @staticmethod
    def _title_property(content: str) -> Dict[str, Any]:
        safe_content = BaseSync._truncate(content)
        return {"title": [{"type": "text", "text": {"content": safe_content}}]}

    @staticmethod
    def _url_property(url: str) -> Dict[str, Any]:
        return {"url": url}

    @staticmethod
    def _multi_select(values: Iterable[str]) -> Dict[str, Any]:
        return {
            "multi_select": [{"name": value} for value in sorted({value for value in values if value})]
        }

    @staticmethod
    def _select(value: Optional[str]) -> Dict[str, Any]:
        return {"select": {"name": value}} if value else {"select": None}

    @staticmethod
    def _people(names: Iterable[str]) -> Dict[str, Any]:
        return {
            "multi_select": [{"name": name} for name in sorted({name for name in names if name})]
        }

    @staticmethod
    def _date_property(date_str: Optional[str]) -> Dict[str, Any]:
        return {"date": {"start": date_str}} if date_str else {"date": None}


class IssueSync(BaseSync):
    def sync(self) -> None:
        issue = self.payload.get("issue")
        if not issue:
            log(logging.WARNING, "Issue payload missing 'issue' key")
            return

        raw_id = issue.get("node_id") or issue.get("id")
        if not raw_id:
            log(logging.WARNING, "Issue payload missing identifier")
            return
        github_id = str(raw_id)
        properties = {
            "Title": self._title_property(issue.get("title", "(no title)")),
            "GitHub ID": self._text_property(github_id),
            "URL": self._url_property(issue.get("html_url", "")),
            "Status": self._select(issue.get("state")),
            "Assignees": self._people(a.get("login") for a in issue.get("assignees", [])),
            "Labels": self._multi_select(label.get("name") for label in issue.get("labels", [])),
            "Updated": self._date_property(issue.get("updated_at")),
            "Created": self._date_property(issue.get("created_at")),
            "Closed": self._date_property(issue.get("closed_at")),
        }
        page_id = self.notion.upsert_page(self.database_id, properties, github_id)
        comments_url = issue.get("comments_url")
        if comments_url:
            self.notifier.ensure_comment(comments_url, page_id)


class PullRequestSync(BaseSync):
    def sync(self) -> None:
        pull = self.payload.get("pull_request")
        if not pull:
            log(logging.WARNING, "Pull request payload missing 'pull_request' key")
            return

        raw_id = pull.get("node_id") or pull.get("id")
        if not raw_id:
            log(logging.WARNING, "Pull request payload missing identifier")
            return
        github_id = str(raw_id)
        properties = {
            "Title": self._title_property(pull.get("title", "(no title)")),
            "GitHub ID": self._text_property(github_id),
            "URL": self._url_property(pull.get("html_url", "")),
            "Status": self._select(pull.get("state")),
            "Draft": {"checkbox": bool(pull.get("draft"))},
            "Assignees": self._people(a.get("login") for a in pull.get("assignees", [])),
            "Labels": self._multi_select(label.get("name") for label in pull.get("labels", [])),
            "Updated": self._date_property(pull.get("updated_at")),
            "Created": self._date_property(pull.get("created_at")),
            "Merged": self._date_property(pull.get("merged_at")),
        }
        page_id = self.notion.upsert_page(self.database_id, properties, github_id)
        comments_url = pull.get("issue_url")
        if comments_url:
            self.notifier.ensure_comment(f"{comments_url}/comments", page_id)


class ProjectSync(BaseSync):
    def sync(self) -> None:
        project = self.payload.get("project") or self.payload.get("project_card") or self.payload.get("project_item")
        if not project:
            log(logging.WARNING, "Project payload missing 'project'/'project_card'/'project_item'")
            return

        raw_id = project.get("node_id") or project.get("id")
        if not raw_id:
            log(logging.WARNING, "Project payload missing identifier")
            return
        github_id = str(raw_id)
        title = project.get("name") or project.get("note") or project.get("content_url", "(project item)")
        properties = {
            "Title": self._title_property(title),
            "GitHub ID": self._text_property(github_id),
            "URL": self._url_property(project.get("html_url") or project.get("url", "")),
            "Status": self._select(project.get("state") or project.get("column_name")),
            "Updated": self._date_property(project.get("updated_at")),
            "Created": self._date_property(project.get("created_at")),
        }
        self.notion.upsert_page(self.database_id, properties, github_id)


class DiscussionSync(BaseSync):
    def sync(self) -> None:
        discussion = self.payload.get("discussion")
        if not discussion:
            log(logging.WARNING, "Discussion payload missing 'discussion'")
            return

        raw_id = discussion.get("node_id") or discussion.get("id")
        if not raw_id:
            log(logging.WARNING, "Discussion payload missing identifier")
            return
        github_id = str(raw_id)
        properties = {
            "Title": self._title_property(discussion.get("title", "(no title)")),
            "GitHub ID": self._text_property(github_id),
            "URL": self._url_property(discussion.get("html_url", "")),
            "Status": self._select(discussion.get("state")),
            "Category": self._select(discussion.get("category", {}).get("name")),
            "Author": self._people([discussion.get("user", {}).get("login")]),
            "Updated": self._date_property(discussion.get("updated_at")),
            "Created": self._date_property(discussion.get("created_at")),
        }
        page_id = self.notion.upsert_page(self.database_id, properties, github_id)
        comments_url = discussion.get("comments_url")
        if comments_url:
            self.notifier.ensure_comment(comments_url, page_id)


HANDLER_MAP = {
    "issues": [IssueSync],
    "issue_comment": [IssueSync],
    "pull_request": [PullRequestSync],
    "pull_request_target": [PullRequestSync],
    "pull_request_review": [PullRequestSync],
    "pull_request_review_comment": [PullRequestSync],
    "project": [ProjectSync],
    "project_card": [ProjectSync],
    "project_column": [ProjectSync],
    "project_item": [ProjectSync],
    "discussion": [DiscussionSync],
    "discussion_comment": [DiscussionSync],
}

DATABASE_ENV_MAP = {
    IssueSync: "NOTION_ISSUES_DB_ID",
    PullRequestSync: "NOTION_PRS_DB_ID",
    ProjectSync: "NOTION_PROJECTS_DB_ID",
    DiscussionSync: "NOTION_DISCUSSIONS_DB_ID",
}


def load_payload(event_path: str) -> Dict[str, Any]:
    try:
        with open(event_path, "r", encoding="utf-8") as file:
            payload = json.load(file)
            log(logging.DEBUG, "Loaded GitHub event payload", keys=list(payload.keys()))
            return payload
    except FileNotFoundError:
        log(logging.ERROR, "GITHUB_EVENT_PATH does not exist", path=event_path)
        raise
    except json.JSONDecodeError as exc:
        log(logging.ERROR, "Failed to parse event payload", error=str(exc))
        raise


def infer_event_name(payload: Dict[str, Any]) -> str:
    if "pull_request" in payload:
        return "pull_request"
    if "issue" in payload:
        return "issues"
    if "discussion" in payload:
        return "discussion"
    if "project_item" in payload:
        return "project_item"
    if "project_card" in payload:
        return "project_card"
    if "project" in payload:
        return "project"
    return ""


def validate_environment(env: Dict[str, str]) -> Dict[str, str]:
    required_keys = {
        "NOTION_TOKEN",
        "NOTION_ISSUES_DB_ID",
        "NOTION_PRS_DB_ID",
        "NOTION_PROJECTS_DB_ID",
        "NOTION_DISCUSSIONS_DB_ID",
    }
    missing = [key for key in required_keys if not env.get(key)]
    if missing:
        log(logging.ERROR, "Missing required environment variables", missing=missing)
        raise RuntimeError("Notion sync configuration is incomplete")
    return {key: env[key] for key in required_keys}


def dispatch(
    event_name: str,
    payload: Dict[str, Any],
    notion: NotionClient,
    notifier: GitHubNotifier,
    env: Dict[str, str],
) -> bool:
    handler_classes = HANDLER_MAP.get(event_name, [])
    if not handler_classes:
        log(logging.INFO, "No handler registered for event", event_name=event_name)
        return True

    all_successful = True
    for handler_cls in handler_classes:
        database_env = DATABASE_ENV_MAP[handler_cls]
        database_id = env[database_env]
        handler = handler_cls(notion, notifier, database_id, payload)
        try:
            handler.sync()
        except Exception as exc:  # pragma: no cover - defensive logging
            all_successful = False
            log(
                logging.ERROR,
                "Handler failed",
                handler=handler_cls.__name__,
                error=str(exc),
            )
    return all_successful


def main() -> int:
    configure_logging()

    event_path = os.environ.get("GITHUB_EVENT_PATH")
    if not event_path:
        log(logging.ERROR, "GITHUB_EVENT_PATH environment variable is not set")
        return 1

    event_name = os.environ.get("GITHUB_EVENT_NAME") or ""
    try:
        payload = load_payload(event_path)
    except Exception:
        return 1

    try:
        env = validate_environment(os.environ)
    except RuntimeError:
        return 1

    notion = NotionClient(env["NOTION_TOKEN"])
    notifier = GitHubNotifier(token=os.environ.get("GITHUB_TOKEN"))

    if not event_name:
        event_name = infer_event_name(payload)
        if event_name:
            log(logging.INFO, "Derived event name from payload structure", event_name=event_name)
        else:
            log(logging.ERROR, "Unable to determine event type from payload")
            return 1

    log(logging.INFO, "Dispatching GitHub event", event_name=event_name)
    try:
        success = dispatch(event_name, payload, notion, notifier, env)
    except Exception as exc:  # pragma: no cover - defensive logging
        log(logging.ERROR, "Failed to process event", error=str(exc))
        return 1

    return 0 if success else 1


if __name__ == "__main__":
    sys.exit(main())
