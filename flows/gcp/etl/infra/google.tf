resource "google_service_account" "prefect_sa" {
  account_id   = var.name
  display_name = var.name
}

resource "google_project_iam_member" "service_account_user" {
  project = var.project_id
  role    = "roles/iam.serviceAccountUser"
  member  = "serviceAccount:${google_service_account.prefect_sa.email}"
}

resource "google_project_iam_member" "run_admin" {
  project = var.project_id
  role    = "roles/run.admin"
  member  = "serviceAccount:${google_service_account.prefect_sa.email}"
}

resource "google_storage_bucket_iam_member" "prefect_sa_storage_object_admin" {
  bucket = google_storage_bucket.prefect_bucket.name
  role   = "roles/storage.objectAdmin"
  member = "serviceAccount:${google_service_account.prefect_sa.email}"
}

resource "google_storage_bucket" "prefect_bucket" {
  name                        = var.name
  location                    = var.region
  force_destroy               = false
  uniform_bucket_level_access = true
}

resource "google_cloud_run_v2_service" "prefect_worker" {
  name     = var.name
  location = var.region

  template {
    containers {
      image = "prefecthq/prefect:3-latest"
      args  = ["prefect", "worker", "start", "--install-policy", "always", "--with-healthcheck", "-p", var.prefect_work_pool_name]

      env {
        name  = "PREFECT_API_URL"
        value = "https://api.prefect.cloud/api/accounts/${var.prefect_account_id}/workspaces/${var.prefect_workspace_id}"
      }

      env {
        name  = "PREFECT_API_KEY"
        value = prefect_service_account.prefect_worker.api_key
      }

      resources {
        cpu_idle = true
        limits = {
          cpu    = "1000m"
          memory = "512Mi"
        }
      }
    }

    service_account = google_service_account.prefect_sa.email

    scaling {
      min_instance_count = 1
    }
  }
}