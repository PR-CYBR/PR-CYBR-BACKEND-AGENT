#############################################
# PR-CYBR Backend Agent Terraform Entrypoint
# All resource configuration should live in
# this module so Terraform Cloud can execute
# init/plan/apply operations from ./infra.
#############################################

terraform {
  required_version = ">= 1.5.0"
}

# Additional providers, data sources, and
# resources will be added as this workspace
# evolves. The module currently focuses on
# variable harmonisation across the fleet.
