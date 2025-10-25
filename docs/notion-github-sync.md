# Notion ↔ GitHub Synchronization Blueprint

This blueprint describes how to cross-reference Notion content with GitHub resources, automate change detection, and keep both systems in sync without triggering feedback loops.

## Cross-Referencing Identifiers

### Storing GitHub Identifiers in Notion
- **Rich text (`GitHub URL`)**: store deep links to repositories, issues, pull requests, or projects so that users can navigate directly from the Notion page.
- **Number (`GitHub ID`)**: capture the immutable GraphQL/REST node identifier for the GitHub resource. This is critical for unambiguous lookups and de-duplication.
- **Select/Multi-select (`GitHub Resource Type`)**: optionally categorize the relationship (Issue, Pull Request, Project Item) to simplify automation filters.
- **Formula (`GitHub Deep Link`)**: concatenate the repository URL with the type and ID to regenerate links when needed.
- Maintain a **`last_synced` date property** to record the timestamp of the last successful synchronization pass.

### Storing Notion Identifiers in GitHub
- **Issue & Pull Request metadata**: add a `Notion-Page-ID` label or issue body footer in the form `Notion Page: [link](https://www.notion.so/<id>)`. For PRs, use the body template or a pinned comment.
- **Project item custom fields**: create a `NotionPageId` text or number field to hold the 32-character Notion page ID without hyphens.
- **Commit trailers**: when commits relate to a Notion task, include `Notion-Page-ID: <id>` in the commit message footer for traceability.

## Change Detection Automation

### GitHub Action (`.github/workflows/notion-pull.yml`)
- **Schedule**: run on a cron (e.g., every 5 minutes) and on manual dispatch.
- **Steps**:
  1. Retrieve the last stored sync cursor/state from the Actions cache, GitHub Encrypted Secrets, or Terraform-managed storage.
  2. Call Notion's [Search](https://developers.notion.com/reference/post-search), [Databases Query](https://developers.notion.com/reference/post-database-query), or [Pages](https://developers.notion.com/reference/get-page) endpoints with the saved cursor to fetch new or updated pages that include GitHub properties.
  3. Compare Notion payload timestamps (`last_edited_time`) with stored metadata to identify changes.
  4. For each change, invoke GitHub REST/GraphQL APIs (issues, pulls, projects) using `actions/github-script` or a custom script to create/update/close matching resources.
  5. Update the sync cursor (`next_cursor`, `last_synced`) and persist it for the next run.
- **Authentication**: use Notion and GitHub tokens delivered via repository secrets or Terraform Cloud workspace environment variables.

### External Sync Service (Alternative)
- Deploy a lightweight worker (e.g., AWS Lambda, Cloud Run, or a container on a schedule) that:
  1. Stores state in DynamoDB/Firestore/PostgreSQL.
  2. Polls Notion on a short interval (respecting rate limits) using saved cursors.
  3. Calls GitHub APIs using a GitHub App installation for higher rate limits and fine-grained permissions.
  4. Optionally pushes updates back to Notion via the Notion API when changes originate in GitHub.
- Infrastructure-as-code (Terraform) can manage credentials, schedules, and storage resources.

## Data Reconciliation & Loop Prevention
- Tag every sync payload with metadata (`last_synced`, `source_system`) to identify the origin of the change.
- When polling Notion:
  - Skip updates whose `last_edited_time` is older than the stored `last_synced` timestamp.
  - If a Notion update includes `last_updated_by` referencing the integration user, assume the change came from GitHub and do not re-apply it.
- When reacting to GitHub events:
  - Store a comment footer or issue body block containing the Notion `last_synced` timestamp. If the incoming GitHub payload matches the existing timestamp, treat it as already synchronized.
  - Use GitHub issue/PR events to record `updated_at` timestamps and compare them with Notion's stored `github_last_update` property.
- Maintain an audit log (e.g., append-only table or Notion database) for debugging conflicts and manual overrides.

## Rate Limits, Pagination, and Tooling
- **Notion API**: default rate limit ~3 requests/second; use exponential backoff and paginate with `start_cursor`/`next_cursor`. Store cursors in cache or Terraform-managed secrets.
- **GitHub API**: REST (5,000 requests/hour for tokens, higher for GitHub Apps); GraphQL uses a points-based system. Batch operations with GraphQL mutations when possible.
- **Pagination**: implement cursor-based iteration for both APIs; persist cursors between runs to avoid re-processing.
- **Tooling/Libraries**:
  - Python: `notion-client`, `PyGithub`, or direct `requests` with typed wrappers.
  - JavaScript/TypeScript: `@notionhq/client`, `@octokit/rest`, or `@octokit/graphql`.
  - Action runners can bundle scripts via `node`/`python` or Docker images (managed in this repo's build system).
- **State Storage**:
  - Lightweight: GitHub Actions cache/artifacts, repository environment secrets, or encrypted files stored via Terraform Cloud.
  - External: AWS S3 + DynamoDB, GCP Cloud Storage + Firestore, or HashiCorp Vault for credentials.
- Monitor rate-limit headers (`X-RateLimit-Remaining`, `Retry-After`) and implement retries with jitter to stay within quotas.

## Governance & Security
- Restrict integration tokens to the minimal scopes: Notion integration with relevant database permissions, GitHub App with Issue, PR, and Project read/write scopes.
- Rotate credentials periodically using Terraform Cloud-managed variables and automated workflows.
- Log sync results in GitHub Actions summaries or external observability tools (CloudWatch, Stackdriver) for auditability.

