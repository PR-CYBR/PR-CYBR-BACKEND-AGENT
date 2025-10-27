#############################################
# PR-CYBR Agent Variable Schema (A-02)
# All sensitive values are provided via
# Terraform Cloud workspace variables.
#############################################

variable "AGENT_ID" {
  type    = string
  default = null
}

variable "PR_CYBR_DOCKER_USER" {
  type    = string
  default = null
}

variable "PR_CYBR_DOCKER_PASS" {
  type      = string
  default   = null
  sensitive = true
}

variable "DOCKERHUB_USERNAME" {
  type    = string
  default = null
}

variable "DOCKERHUB_TOKEN" {
  type      = string
  default   = null
  sensitive = true
}

variable "GLOBAL_DOMAIN" {
  type    = string
  default = null
}

variable "AGENT_ACTIONS" {
  type      = string
  default   = null
  sensitive = true
}

variable "NOTION_TOKEN" {
  type      = string
  default   = null
  sensitive = true
}

variable "NOTION_DISCUSSIONS_ARC_DB_ID" {
  type    = string
  default = null
}

variable "NOTION_ISSUES_BACKLOG_DB_ID" {
  type    = string
  default = null
}

variable "NOTION_KNOWLEDGE_FILE_DB_ID" {
  type    = string
  default = null
}

variable "NOTION_PROJECT_BOARD_BACKLOG_DB_ID" {
  type    = string
  default = null
}

variable "NOTION_PR_BACKLOG_DB_ID" {
  type    = string
  default = null
}

variable "NOTION_TASK_BACKLOG_DB_ID" {
  type    = string
  default = null
}

variable "NOTION_PAGE_ID" {
  type    = string
  default = null
}

variable "TFC_TOKEN" {
  type      = string
  default   = null
  sensitive = true
}
