variable "name" {
  description = "The name to use for resources"
  default     = "prefect-worker"
}

variable "project_id" {
  description = "The ID of the GCP project"
}

variable "region" {
  description = "The name of the GCP region"
  default     = "us-central1"
}

variable "prefect_account_id" {
  description = "The Prefect account ID"
}

variable "prefect_workspace_id" {
  description = "The Prefect workspace ID"
}

variable "prefect_api_key" {
  description = "The Prefect API key for provisioning resources"
  sensitive   = true
}

variable "prefect_work_pool_name" {
  description = "The name of the Prefect work pool"
  default     = "cloud-run-v2"
}
