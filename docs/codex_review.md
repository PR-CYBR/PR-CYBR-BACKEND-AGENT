# Codex Review Playbook

The Codex review cadence ensures that every proposed change is evaluated against workflow quality, documentation depth, and dashboard continuity.

## Review Triggers
- **Pull request scans** fire the `codex-pr-scan` workflow to verify policy alignment and artifact completeness.
- **Commit discussions** recorded by `codex-commit-discussions` surface high-signal conversations for reviewers.
- **Wiki updates** via `codex-wiki-updates` alert reviewers to evolving operational docs.

## Reviewer Checklist
1. Confirm that automation workflows describe actionable steps for downstream agents.
2. Verify the `sync_matrix.yml` reflects any new inter-agent dependencies.
3. Ensure dashboard guidance references current configuration options found in `dashboard_config.json`.
4. Capture observations in the `codex_report.md` status log.

## Outcomes
Reviews culminate in one of three states:
- **Ready** – changes align with workflow requirements and dashboard integration expectations.
- **Needs Iteration** – author must address gaps called out during scan or manual review.
- **Deferred** – change is blocked pending external dependencies surfaced in the sync matrix.
