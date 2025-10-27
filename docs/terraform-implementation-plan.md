# A-02 Terraform & Workflow Alignment Plan

- **Last Updated:** 2025-10-27
- **Owner:** PR-CYBR Backend Agent Automation Initiative

## Scope of Changes
- Relocate all Terraform configuration files into `infra/`.
- Standardise variable declarations via `infra/agent-variables.tf` and `infra/variables.tfvars`.
- Align GitHub Action workflows to execute Terraform from `./infra`.
- Remove or refactor any legacy variables no longer supported by Terraform Cloud.

## File & Directory Updates
1. `infra/agent-variables.tf`
   - Houses the authoritative list of Terraform variables for the workspace.
2. `infra/main.tf`
   - Entry module to host Terraform settings and future resources.
3. `infra/variables.tfvars`
   - Reference map of workspace variables managed in Terraform Cloud / GitHub Secrets.
4. `.github/workflows/tfc-sync.yml`
   - Updated to run Terraform commands within the `./infra` directory.

## Variable Harmonisation
- **Retained:** `AGENT_ACTIONS`, `AGENT_COLLAB`, `DOCKERHUB_TOKEN`, `DOCKERHUB_USERNAME`, `GLOBAL_DOMAIN`, `GLOBAL_ELASTIC_URI`, `GLOBAL_GRAFANA_URI`, `GLOBAL_KIBANA_URI`, `GLOBAL_PROMETHEUS_URI`, `GLOBAL_TAILSCALE_AUTHKEY`, `GLOBAL_TRAEFIK_ACME_EMAIL`, `GLOBAL_TRAEFIK_ENTRYPOINTS`, `GLOBAL_ZEROTIER_NETWORK_ID`.
- **Deprecated / Removed:** No additional legacy variables detected in the repository at audit time.

## Workflow Adjustments
- `tfc-sync.yml`: Added `working-directory: ./infra` to `terraform init`, `terraform plan`, and `terraform apply` steps.
- No other workflows currently invoke Terraform commands.

## Validation Steps
1. From the repository root, run `terraform -chdir=infra init`.
2. Execute `terraform -chdir=infra plan` to confirm variable resolution via Terraform Cloud workspace variables.
3. Trigger the GitHub Action **tfc-sync / terraform** and verify successful `init`, `plan`, and `apply` phases.

> Note: Terraform Cloud manages sensitive values; ensure workspace environment variables remain in sync with the keys listed above.
