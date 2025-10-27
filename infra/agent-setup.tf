########################################################
# PR-CYBR Agent Terraform Bootstrap (Environment A-02)
#
# This configuration intentionally avoids defining any
# remote backends or providers. Terraform Cloud supplies
# all workspace variables, which are aggregated below for
# downstream modules and GitHub Actions secrets syncing.
########################################################

terraform {
  required_version = ">= 1.5.0"
}

locals {
  agent_configuration = {
    agent_id                           = var.AGENT_ID
    pr_cybr_docker_user                = var.PR_CYBR_DOCKER_USER
    pr_cybr_docker_pass                = var.PR_CYBR_DOCKER_PASS
    dockerhub_username                 = var.DOCKERHUB_USERNAME
    dockerhub_token                    = var.DOCKERHUB_TOKEN
    global_domain                      = var.GLOBAL_DOMAIN
    agent_actions                      = var.AGENT_ACTIONS
    notion_token                       = var.NOTION_TOKEN
    notion_discussions_arc_db_id       = var.NOTION_DISCUSSIONS_ARC_DB_ID
    notion_issues_backlog_db_id        = var.NOTION_ISSUES_BACKLOG_DB_ID
    notion_knowledge_file_db_id        = var.NOTION_KNOWLEDGE_FILE_DB_ID
    notion_project_board_backlog_db_id = var.NOTION_PROJECT_BOARD_BACKLOG_DB_ID
    notion_pr_backlog_db_id            = var.NOTION_PR_BACKLOG_DB_ID
    notion_task_backlog_db_id          = var.NOTION_TASK_BACKLOG_DB_ID
    notion_page_id                     = var.NOTION_PAGE_ID
    tfc_token                          = var.TFC_TOKEN
  }
}

output "agent_configuration" {
  description = "Aggregated agent configuration sourced from Terraform Cloud variables."
  value       = local.agent_configuration
  sensitive   = true
}
