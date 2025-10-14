# Codex Workflow Dashboard

This Flask application visualizes the automation workflows that coordinate Codex agents.

## Getting Started
1. Create a virtual environment and install requirements:
   ```bash
   python -m venv .venv
   source .venv/bin/activate
   pip install flask
   ```
2. Launch the dashboard:
   ```bash
   export FLASK_APP=dashboard.app:create_app
   flask run --debug
   ```
3. Open `http://127.0.0.1:5000` in your browser to inspect workflow metadata defined in `dashboard_config.json`.

## Configuration
- Update `dashboard_config.json` to register new workflows, triggers, or dependencies.
- Align configuration changes with the inter-agent mapping stored in `docs/sync_matrix.yml`.

## API Surface
- `GET /api/workflows` – returns the list of workflows displayed on the landing page.
- `GET /api/workflows/<name>` – returns detail for a specific workflow.

For additional integration guidance, review `docs/dashboard_integration.md`.
