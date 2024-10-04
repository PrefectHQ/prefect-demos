data "prefect_worker_metadata" "d" {}

resource "prefect_service_account" "prefect_worker" {
  name              = var.name
  account_role_name = "Member"
}

data "prefect_workspace_role" "worker" {
  name       = "Worker"
  account_id = var.prefect_account_id
}

resource "prefect_workspace_access" "worker_access" {
  accessor_type     = "SERVICE_ACCOUNT"
  accessor_id       = prefect_service_account.prefect_worker.id
  workspace_id      = var.prefect_workspace_id
  workspace_role_id = data.prefect_workspace_role.worker.id
}

resource "prefect_work_pool" "cloud_run_pool" {
  name   = var.prefect_work_pool_name
  type   = "cloud-run-v2"
  paused = false

  # Merge the default cloud run base job template with custom variables
  base_job_template = jsonencode(merge(
    jsondecode(data.prefect_worker_metadata.d.base_job_configs.cloud_run_v2),
    {
      variables = merge(
        jsondecode(data.prefect_worker_metadata.d.base_job_configs.cloud_run_v2).variables,
        {
          properties = merge(
            jsondecode(data.prefect_worker_metadata.d.base_job_configs.cloud_run_v2).variables.properties,
            {
              # Anything in variables can be set here
              for key, value in {
                cpu                  = "1000m",
                memory               = "2Gi",
                image                = "prefecthq/prefect:3-latest",
                region               = var.region,
                service_account_name = google_service_account.prefect_sa.email
                } : key => merge(
                jsondecode(data.prefect_worker_metadata.d.base_job_configs.cloud_run_v2).variables.properties[key],
                { default = value }
              )
            }
          )
        }
      )
    }
  ))
}
