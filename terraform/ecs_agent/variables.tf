variable "vpc_id" {
  description = "VPC ID in which to create all resources"
  type        = string
}

variable "agent_subnets" {
  description = "Subnets to place the agent in"
  type        = list(string)
}

variable "prefect_account_id" {
  description = "Prefect cloud account ID"
  type        = string
}

variable "prefect_api_key" {
  description = "Prefect cloud API key"
  type        = string
  sensitive   = true
}

variable "prefect_workspace_id" {
  description = "Prefect cloud workspace ID"
  type        = string
}

