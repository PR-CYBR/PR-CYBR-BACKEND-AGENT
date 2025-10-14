# Dashboard and Workflow Integration Guide

The `dashboard/` Flask application surfaces Codex automation telemetry via a lightweight REST API and HTML interface.

## Configuration Flow
1. Workflow metadata is defined in `dashboard/dashboard_config.json`.
2. `dashboard.app.load_configuration` reads the JSON file and converts each entry into a `WorkflowSummary` dataclass.
3. The `/api/workflows` endpoint returns the serialized configuration for consumption by the browser client or external agents.
4. The browser module (`dashboard/static/js/dashboard.js`) fetches workflow details and renders them in the UI.

## Interaction with GitHub Workflows
- **codex-pr-scan** exposes scan health so reviewers can inspect status during PR evaluations.
- **codex-commit-discussions** provides commit comment digests that appear in the dashboard's detail pane.
- **codex-wiki-updates** notifies the dashboard when knowledge-base artifacts change, enabling dynamic update messaging.
- **codex-setup-maintenance** publishes maintenance logs that the dashboard can surface for operational tracking.

## Extending the GUI
- Add new workflow definitions to `dashboard_config.json` to display additional automation.
- Extend the Flask API to proxy live metrics (e.g., read action artifacts) for deeper analytics.
- Update the sync matrix (`docs/sync_matrix.yml`) whenever new dependencies are introduced so the dashboard can mirror relationships accurately.
