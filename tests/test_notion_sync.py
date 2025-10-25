import json
from unittest import mock

import pytest

from shared.notion_sync import (
    NotionSyncClient,
    NotionSyncError,
    NotionSyncPayload,
    build_notion_request,
    parse_payload,
)


def test_parse_payload_success():
    raw = {
        "id": 42,
        "title": "Demo issue",
        "html_url": "https://github.com/example/repo/issues/42",
        "status": "Open",
        "github_metadata": {"labels": ["bug"]},
    }

    payload = parse_payload(raw)

    assert isinstance(payload, NotionSyncPayload)
    assert payload.item_id == "42"
    assert payload.title == "Demo issue"
    assert payload.status == "Open"
    assert payload.github_metadata == {"labels": ["bug"]}


def test_parse_payload_missing_required_fields():
    with pytest.raises(ValueError) as excinfo:
        parse_payload({"id": 1, "title": "Missing bits"})

    assert "missing required fields" in str(excinfo.value)


def test_build_notion_request_round_trip():
    payload = NotionSyncPayload(
        item_id="123",
        title="Hello",
        html_url="https://github.com/example/repo/issues/123",
        status="In Progress",
        github_metadata={"assignee": "octocat"},
    )

    request_body = build_notion_request(payload, database_id="db-1")

    assert request_body["parent"]["database_id"] == "db-1"
    properties = request_body["properties"]
    assert properties["Name"]["title"][0]["text"]["content"] == "Hello"
    assert properties["Status"]["select"]["name"] == "In Progress"
    assert properties["Source"]["url"] == payload.html_url
    metadata = properties["GitHub Metadata"]["rich_text"][0]["text"]["content"]
    assert json.loads(metadata) == payload.github_metadata


def test_client_retries_then_succeeds(caplog):
    session = mock.Mock()
    responses = [
        mock.Mock(status_code=429, ok=False, text="rate limit"),
        mock.Mock(status_code=500, ok=False, text="server error"),
        mock.Mock(status_code=200, ok=True, json=lambda: {"id": "notion-page"}),
    ]
    session.request.side_effect = responses

    client = NotionSyncClient("token", session=session, max_retries=5, backoff_factor=0)

    with mock.patch("time.sleep") as sleep:
        result = client.upsert_page({"properties": {}}, page_id=None)

    assert result == {"id": "notion-page"}
    assert session.request.call_count == 3
    # Ensure exponential backoff attempted twice (attempts before success)
    assert sleep.call_count == 2

    warning_records = [record for record in caplog.records if record.levelname == "WARNING"]
    assert any(record.status == 429 for record in warning_records)
    assert any(record.status == 500 for record in warning_records)


def test_client_raises_after_exhausting_retries(caplog):
    session = mock.Mock()
    session.request.return_value = mock.Mock(status_code=503, ok=False, text="unavailable")

    client = NotionSyncClient("token", session=session, max_retries=2, backoff_factor=0)

    with pytest.raises(NotionSyncError) as excinfo:
        client.upsert_page({"properties": {}})

    assert "Exceeded maximum retries" in str(excinfo.value)
    assert session.request.call_count == 2

    warning_records = [record for record in caplog.records if record.levelname == "WARNING"]
    assert len(warning_records) >= 2
    assert all(record.status == 503 for record in warning_records)

