provider "google" {
  project = var.project_id
  region  = var.region
}

provider "prefect" {
  api_key      = var.prefect_api_key
  account_id   = var.prefect_account_id
  workspace_id = var.prefect_workspace_id
}