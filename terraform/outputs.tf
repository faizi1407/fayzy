output "frontend_url" {
  description = "URL of the frontend Cloud Run service"
  value       = google_cloud_run_v2_service.frontend.uri
}

output "backend_url" {
  description = "URL of the backend Cloud Run service"
  value       = google_cloud_run_v2_service.backend.uri
}

output "frontend_service_name" {
  description = "Name of the frontend Cloud Run service"
  value       = google_cloud_run_v2_service.frontend.name
}

output "backend_service_name" {
  description = "Name of the backend Cloud Run service"
  value       = google_cloud_run_v2_service.backend.name
}

output "frontend_service_account_email" {
  description = "Email of the frontend service account"
  value       = google_service_account.frontend.email
}

output "backend_service_account_email" {
  description = "Email of the backend service account"
  value       = google_service_account.backend.email
}
