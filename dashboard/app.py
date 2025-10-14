"""Flask application that visualizes Codex workflow activity."""

from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, List

from flask import Flask, jsonify, render_template


CONFIG_FILENAME = "dashboard_config.json"


@dataclass
class WorkflowSummary:
    """Representation of workflow metadata consumed by the dashboard."""

    name: str
    description: str
    owner: str
    triggers: List[str]
    dependencies: List[str]

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "WorkflowSummary":
        return cls(
            name=data.get("name", "unknown"),
            description=data.get("description", ""),
            owner=data.get("owner", "unassigned"),
            triggers=list(data.get("triggers", [])),
            dependencies=list(data.get("dependencies", [])),
        )


def load_configuration(config_path: Path) -> Dict[str, Any]:
    if not config_path.exists():
        raise FileNotFoundError(f"Dashboard configuration not found at {config_path}")

    with config_path.open("r", encoding="utf-8") as handle:
        payload = json.load(handle)

    workflows = [WorkflowSummary.from_dict(item) for item in payload.get("workflows", [])]
    payload["workflows"] = workflows
    return payload


def create_app(config_path: Path | None = None) -> Flask:
    """Factory used by WSGI servers and the Flask CLI."""

    app = Flask(__name__, template_folder="templates", static_folder="static")

    resolved_path = config_path or Path(__file__).resolve().parent / CONFIG_FILENAME
    config = load_configuration(resolved_path)

    @app.route("/")
    def index() -> str:
        return render_template("index.html", workflows=config["workflows"])

    @app.route("/api/workflows")
    def workflows_api() -> Any:
        serialized = [workflow.__dict__ for workflow in config["workflows"]]
        return jsonify({"workflows": serialized})

    @app.route("/api/workflows/<workflow_name>")
    def workflow_detail(workflow_name: str) -> Any:
        workflow = next((wf for wf in config["workflows"] if wf.name == workflow_name), None)
        if workflow is None:
            return jsonify({"error": "workflow not found"}), 404
        return jsonify({"workflow": workflow.__dict__})

    return app


if __name__ == "__main__":
    flask_app = create_app()
    flask_app.run(host="0.0.0.0", port=8000, debug=True)
