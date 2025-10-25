# Notion Sync Dry-Run & Recovery Procedure

This runbook describes how to validate the GitHub → Notion synchronisation
pipeline without touching production data.  It mirrors the operational pattern
defined in the [`spec-bootstrap`](https://github.com/PR-CYBR/spec-bootstrap/)
repository and should be executed whenever significant sync changes (parsing,
workflow, retry logic) are introduced.

## 1. Prepare a Feature Branch

1. Branch from `codex` (or the integration branch that mirrors `spec-bootstrap`)
   and push your changes there.  Example: `feature/notion-sync-hardening`.
2. Open a pull request targeting `codex`.  This keeps CI/CD and branch
   protections intact while avoiding direct pushes to `main`.

## 2. Create Sandbox GitHub Artifacts

Perform these actions inside a temporary testing repository or a dedicated
sandbox area:

- **Issues** – create at least one issue with labels, assignees and a milestone
  to exercise metadata parsing.
- **Pull Requests** – open a PR, include reviewer assignments and link to the
  issue.
- **Discussions** – create a short discussion thread that matches the format the
  sync consumes.
- **Projects** – add a draft item to the project board the sync integrates with
  (e.g., add the issue or PR to the board).

Record the URLs for each artifact; they will be referenced in the dry-run
results.

## 3. Execute the Dry Run

1. In GitHub Actions, manually trigger the `setup-dry-run` workflow for your
   feature branch.
2. Export the required environment variables (e.g., Notion integration token,
   database IDs) via Terraform Cloud workspace variables so secrets remain out of
   the repository.
3. Point the sync script to the sandbox GitHub repository and the Notion test
   database. Provide a GitHub token with the minimum scopes possible—prefer a
   repository-scoped PAT stored as `READ_ONLY_GITHUB_TOKEN` when the workflow
   needs to perform writebacks.
4. Run the synchronisation script in dry-run mode (no writes) if available; if
   not, ensure the Notion integration uses a staging database.

## 4. Verify Notion Updates

After the dry run completes:

1. Confirm new or updated Notion pages appear in the sandbox database.
2. Validate that properties match the sandbox GitHub artifacts (titles, URLs,
   statuses, metadata JSON blob).
3. Capture screenshots for audit purposes and attach them to the PR or release
   notes.

## 5. Rollback & Cleanup

If anything misbehaves:

- Revert the feature branch or roll back the deployment using the normal PR
  process.
- Remove sandbox data in both GitHub and Notion.
- If the script performed writes in production by accident, use the captured
  IDs to remove or correct the affected Notion pages.
- Open an incident ticket documenting what happened and link to the logs.

Finally, delete the sandbox GitHub artifacts and close the test PR once
validation is complete.

## 6. Monitoring & Alerts

- Monitor the first few scheduled runs after merging by inspecting the workflow
  logs and Notion database.
- Configure alerts (e.g., GitHub Action notifications or Slack webhooks) that
  trigger on workflow failure so the team can react quickly.
- Continue to run periodic dry runs whenever major schema or API changes occur.

