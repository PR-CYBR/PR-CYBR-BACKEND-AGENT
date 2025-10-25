"""Utilities for synchronising GitHub activity with Notion.

This module intentionally keeps the functionality self contained so that we
can exercise it through unit tests without touching the network.  The
``NotionSyncClient`` encapsulates resiliency concerns, including retry and
backoff logic, while helper functions normalise payload parsing and request
construction.
"""

from __future__ import annotations

import json
import logging
import time
from dataclasses import dataclass
from typing import Any, Dict, Mapping, MutableMapping, Optional
from urllib.parse import urljoin

import requests


logger = logging.getLogger(__name__)


class NotionSyncError(RuntimeError):
    """Raised when a Notion synchronisation attempt fails."""


@dataclass(frozen=True)
class NotionSyncPayload:
    """Strongly typed representation of the GitHub webhook payload.

    The GitHub payloads we consume contain a mix of GitHub specific metadata
    along with display information we want to surface inside Notion.  Normalising
    the structure allows the rest of the synchronisation code to stay agnostic of
    the raw payload layout.
    """

    item_id: str
    title: str
    html_url: str
    status: str
    github_metadata: Dict[str, Any]


def parse_payload(raw_payload: Mapping[str, Any]) -> NotionSyncPayload:
    """Parse a GitHub payload into :class:`NotionSyncPayload`.

    Parameters
    ----------
    raw_payload:
        The inbound payload, typically derived from a webhook body.

    Returns
    -------
    NotionSyncPayload

    Raises
    ------
    ValueError
        If the payload is missing required fields.
    """

    required_fields = ["id", "title", "html_url", "status"]
    missing = [field for field in required_fields if field not in raw_payload]
    if missing:
        raise ValueError(f"Payload is missing required fields: {', '.join(missing)}")

    github_metadata = dict(raw_payload.get("github_metadata", {}))

    return NotionSyncPayload(
        item_id=str(raw_payload["id"]),
        title=str(raw_payload["title"]),
        html_url=str(raw_payload["html_url"]),
        status=str(raw_payload["status"]),
        github_metadata=github_metadata,
    )


def build_notion_request(payload: NotionSyncPayload, database_id: str) -> Dict[str, Any]:
    """Construct the request body for Notion's ``pages`` endpoint."""

    properties: Dict[str, Any] = {
        "Name": {
            "title": [
                {
                    "text": {
                        "content": payload.title,
                    }
                }
            ]
        },
        "Status": {
            "select": {
                "name": payload.status,
            }
        },
        "Source": {
            "url": payload.html_url,
        },
        "GitHub Metadata": {
            "rich_text": [
                {
                    "text": {
                        "content": json.dumps(payload.github_metadata, sort_keys=True),
                    }
                }
            ]
        },
    }

    return {
        "parent": {"database_id": database_id},
        "properties": properties,
    }


class NotionSyncClient:
    """Client wrapper that handles retry, backoff and logging."""

    RETRY_STATUS_CODES = {429, 500, 502, 503, 504}

    def __init__(
        self,
        token: str,
        *,
        base_url: str = "https://api.notion.com/v1/",
        session: Optional[requests.Session] = None,
        max_retries: int = 5,
        backoff_factor: float = 1.0,
        timeout: float = 10.0,
    ) -> None:
        self.base_url = base_url
        self.session = session or requests.Session()
        self.max_retries = max(1, max_retries)
        self.backoff_factor = max(0.0, backoff_factor)
        self.timeout = timeout
        self.headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
            "Notion-Version": "2022-06-28",
        }

    def upsert_page(self, payload: MutableMapping[str, Any], page_id: Optional[str] = None) -> Dict[str, Any]:
        """Create or update a Notion page.

        Parameters
        ----------
        payload:
            The request body returned by :func:`build_notion_request`.
        page_id:
            Optional Notion page identifier.  When provided the request becomes a
            PATCH to update the page, otherwise a POST creates a new page.
        """

        method = "patch" if page_id else "post"
        endpoint = f"pages/{page_id}" if page_id else "pages"
        return self._request(method, endpoint, json=payload)

    # The ``json`` keyword matches ``requests.Session.request`` signature, which
    # simplifies mocking in the unit tests.
    def _request(self, method: str, path: str, *, json: MutableMapping[str, Any]) -> Dict[str, Any]:  # noqa: A003
        url = urljoin(self.base_url, path)

        for attempt in range(1, self.max_retries + 1):
            try:
                response = self.session.request(
                    method=method.upper(),
                    url=url,
                    headers=self.headers,
                    json=json,
                    timeout=self.timeout,
                )
            except requests.RequestException as exc:  # pragma: no cover - defensive
                logger.error(
                    "Notion API request raised exception",
                    extra={"attempt": attempt, "url": url, "error": str(exc)},
                )
                if attempt == self.max_retries:
                    raise NotionSyncError("Notion API request failed due to network error") from exc
                self._sleep(attempt)
                continue

            if response.status_code in self.RETRY_STATUS_CODES:
                logger.warning(
                    "Notion API transient error",
                    extra={
                        "attempt": attempt,
                        "status": response.status_code,
                        "url": url,
                    },
                )
                if attempt == self.max_retries:
                    break
                self._sleep(attempt)
                continue

            if response.ok:
                logger.info(
                    "Notion API request succeeded",
                    extra={
                        "attempt": attempt,
                        "status": response.status_code,
                        "url": url,
                    },
                )
                try:
                    return response.json()
                except ValueError:
                    return {}

            logger.error(
                "Notion API request failed",
                extra={
                    "attempt": attempt,
                    "status": response.status_code,
                    "url": url,
                    "body": response.text,
                },
            )
            raise NotionSyncError(
                f"Notion API request failed with status {response.status_code}: {response.text}"
            )

        raise NotionSyncError("Exceeded maximum retries for Notion API request")

    def _sleep(self, attempt: int) -> None:
        delay = self.backoff_factor * (2 ** (attempt - 1))
        logger.debug("Sleeping before retry", extra={"attempt": attempt, "delay": delay})
        time.sleep(delay)


__all__ = [
    "NotionSyncClient",
    "NotionSyncError",
    "NotionSyncPayload",
    "build_notion_request",
    "parse_payload",
]

