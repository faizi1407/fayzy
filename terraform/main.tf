terraform {
  required_version = ">= 1.5.0"

  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "~> 5.0"
    }
  }
}

provider "google" {
  project = var.project_id
  region  = var.region
}

# Service Account for Frontend
resource "google_service_account" "frontend" {
  account_id   = "frontend-cloudrun-sa"
  display_name = "Frontend Cloud Run Service Account"
  description  = "Service account for frontend Cloud Run service with least-privilege permissions"
}

# Service Account for Backend
resource "google_service_account" "backend" {
  account_id   = "backend-cloudrun-sa"
  display_name = "Backend Cloud Run Service Account"
  description  = "Service account for backend Cloud Run service with least-privilege permissions"
}

# IAM binding for backend to access Secret Manager
resource "google_project_iam_member" "backend_secret_accessor" {
  project = var.project_id
  role    = "roles/secretmanager.secretAccessor"
  member  = "serviceAccount:${google_service_account.backend.email}"
}

# IAM binding for frontend to access Secret Manager
resource "google_project_iam_member" "frontend_secret_accessor" {
  project = var.project_id
  role    = "roles/secretmanager.secretAccessor"
  member  = "serviceAccount:${google_service_account.frontend.email}"
}

# Frontend Cloud Run Service
resource "google_cloud_run_v2_service" "frontend" {
  name     = var.frontend_service_name
  location = var.region
  ingress  = "INGRESS_TRAFFIC_ALL"

  template {
    service_account = google_service_account.frontend.email

    scaling {
      min_instance_count = 0
      max_instance_count = var.frontend_max_instances
    }

    containers {
      image = var.frontend_image

      ports {
        container_port = var.frontend_port
      }

      resources {
        limits = {
          cpu    = var.frontend_cpu
          memory = var.frontend_memory
        }
        cpu_idle          = true
        startup_cpu_boost = true
      }

      startup_probe {
        http_get {
          path = var.frontend_health_check_path
          port = var.frontend_port
        }
        initial_delay_seconds = 0
        timeout_seconds       = 1
        period_seconds        = 3
        failure_threshold     = 3
      }

      liveness_probe {
        http_get {
          path = var.frontend_health_check_path
          port = var.frontend_port
        }
        initial_delay_seconds = 0
        timeout_seconds       = 1
        period_seconds        = 10
        failure_threshold     = 3
      }

      dynamic "env" {
        for_each = var.frontend_env_vars
        content {
          name  = env.key
          value = env.value
        }
      }

      dynamic "env" {
        for_each = var.frontend_secret_env_vars
        content {
          name = env.key
          value_source {
            secret_key_ref {
              secret  = env.value.secret
              version = env.value.version
            }
          }
        }
      }
    }

    timeout = "300s"

    max_instance_request_concurrency = var.frontend_max_concurrency
  }

  traffic {
    type    = "TRAFFIC_TARGET_ALLOCATION_TYPE_LATEST"
    percent = 100
  }

  depends_on = [
    google_project_iam_member.frontend_secret_accessor
  ]
}

# Backend Cloud Run Service
resource "google_cloud_run_v2_service" "backend" {
  name     = var.backend_service_name
  location = var.region
  ingress  = "INGRESS_TRAFFIC_ALL"

  template {
    service_account = google_service_account.backend.email

    scaling {
      min_instance_count = 0
      max_instance_count = var.backend_max_instances
    }

    containers {
      image = var.backend_image

      ports {
        container_port = var.backend_port
      }

      resources {
        limits = {
          cpu    = var.backend_cpu
          memory = var.backend_memory
        }
        cpu_idle          = true
        startup_cpu_boost = true
      }

      startup_probe {
        http_get {
          path = var.backend_health_check_path
          port = var.backend_port
        }
        initial_delay_seconds = 0
        timeout_seconds       = 1
        period_seconds        = 3
        failure_threshold     = 3
      }

      liveness_probe {
        http_get {
          path = var.backend_health_check_path
          port = var.backend_port
        }
        initial_delay_seconds = 0
        timeout_seconds       = 1
        period_seconds        = 10
        failure_threshold     = 3
      }

      dynamic "env" {
        for_each = var.backend_env_vars
        content {
          name  = env.key
          value = env.value
        }
      }

      dynamic "env" {
        for_each = var.backend_secret_env_vars
        content {
          name = env.key
          value_source {
            secret_key_ref {
              secret  = env.value.secret
              version = env.value.version
            }
          }
        }
      }
    }

    timeout = "300s"

    max_instance_request_concurrency = var.backend_max_concurrency
  }

  traffic {
    type    = "TRAFFIC_TARGET_ALLOCATION_TYPE_LATEST"
    percent = 100
  }

  depends_on = [
    google_project_iam_member.backend_secret_accessor
  ]
}

# IAM policy to allow public access to frontend
resource "google_cloud_run_v2_service_iam_member" "frontend_public" {
  count    = var.frontend_allow_public_access ? 1 : 0
  project  = google_cloud_run_v2_service.frontend.project
  location = google_cloud_run_v2_service.frontend.location
  name     = google_cloud_run_v2_service.frontend.name
  role     = "roles/run.invoker"
  member   = "allUsers"
}

# IAM policy to allow public access to backend
resource "google_cloud_run_v2_service_iam_member" "backend_public" {
  count    = var.backend_allow_public_access ? 1 : 0
  project  = google_cloud_run_v2_service.backend.project
  location = google_cloud_run_v2_service.backend.location
  name     = google_cloud_run_v2_service.backend.name
  role     = "roles/run.invoker"
  member   = "allUsers"
}
