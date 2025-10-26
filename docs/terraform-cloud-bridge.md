# Terraform Cloud – GitHub Workflow Bridge (Template A-02)

The Terraform Cloud – GitHub workflow bridge keeps all sensitive credentials in Terraform Cloud while allowing GitHub Actions to trigger remote runs.

This repository now includes the `terraform-cloud-bridge` workflow located at `.github/workflows/terraform-cloud-bridge.yml`. The workflow is based on template **A-02** and expects the organization to configure the following repository variables so that GitHub can request short-lived workflow tokens from Terraform Cloud using OpenID Connect (OIDC).

| Variable | Required | Description |
| --- | --- | --- |
| `TFC_HOSTNAME` | No (defaults to `app.terraform.io`) | Terraform Cloud hostname if using Terraform Enterprise. |
| `TFC_ORGANIZATION` | Yes | Terraform Cloud organization name. |
| `TFC_WORKSPACE_NAME` | Yes | Terraform Cloud workspace to trigger. |
| `TFC_PROJECT_ID` | Optional | Terraform Cloud project identifier if the workspace is scoped to a project. |
| `TFC_CONFIGURATION_DIRECTORY` | Optional | Relative directory containing Terraform configuration. Defaults to repository root. |
| `TFC_WORKFLOW_ID` | Yes | Identifier of the Terraform Cloud workflow bridge configuration. |
| `TFC_WORKFLOW_AUDIENCE` | Yes | OIDC audience value provided by Terraform Cloud when the workflow bridge is created. |
| `TFC_TOKEN_EXCHANGE_URL` | Yes | Terraform Cloud endpoint that exchanges GitHub OIDC tokens for short-lived workflow tokens. |
| `TFC_RUN_ENDPOINT` | Yes | Terraform Cloud API endpoint that queues runs for the workspace. |

> **Note:** The template intentionally requires configuration through Terraform Cloud so that secrets and long-lived tokens remain inside Terraform Cloud. GitHub only receives ephemeral workflow tokens when each run executes.

## Terraform Cloud configuration checklist

1. **Create or update the Terraform Cloud workspace.**
   - Connect the workspace to this GitHub repository using the native VCS integration.
   - Store all environment variables, Terraform variables, and credentials within Terraform Cloud.

2. **Enable the Terraform Cloud workflow bridge.**
   - From the Terraform Cloud organization settings, create a new GitHub workflow bridge targeting the workspace.
   - Capture the `workflow_id`, `token exchange URL`, `run endpoint`, and `OIDC audience` values produced during setup.

3. **Populate GitHub repository variables.**
   - Navigate to *Settings → Secrets and variables → Actions → Variables*.
   - Create the variables listed in the table above using the values supplied by Terraform Cloud.
   - No GitHub secrets are required; all sensitive data stays in Terraform Cloud.

4. **(Optional) Restrict workflow execution.**
   - Apply branch protection or GitHub environment rules to limit who can trigger Terraform Cloud runs.

5. **Verify the bridge.**
   - Open a pull request or push to a tracked branch.
   - The GitHub workflow should exchange an OIDC token for a Terraform Cloud workflow token and queue a remote run. Review the Terraform Cloud UI to confirm that runs execute successfully.

## Run visibility

Each workflow execution writes a summary entry that includes the Terraform Cloud run identifier. The summary links directly to the remote run so reviewers can monitor plan and apply progress without exposing credentials in GitHub.

