variable "project_id" {
  description = "GCP Project ID"
  type        = string
}

variable "region" {
  description = "GCP region for Cloud Run services"
  type        = string
  default     = "us-central1"
}

# Frontend Service Variables
variable "frontend_service_name" {
  description = "Name of the frontend Cloud Run service"
  type        = string
  default     = "frontend"
}

variable "frontend_image" {
  description = "Container image for frontend service"
  type        = string
}

variable "frontend_port" {
  description = "Port the frontend container listens on"
  type        = number
  default     = 8080
}

variable "frontend_cpu" {
  description = "CPU allocation for frontend (e.g., '1000m' for 1 vCPU)"
  type        = string
  default     = "1000m"
}

variable "frontend_memory" {
  description = "Memory allocation for frontend (e.g., '512Mi')"
  type        = string
  default     = "512Mi"
}

variable "frontend_max_instances" {
  description = "Maximum number of frontend instances"
  type        = number
  default     = 10
}

variable "frontend_max_concurrency" {
  description = "Maximum concurrent requests per frontend instance"
  type        = number
  default     = 80
}

variable "frontend_health_check_path" {
  description = "Health check path for frontend service"
  type        = string
  default     = "/"
}

variable "frontend_env_vars" {
  description = "Environment variables for frontend service"
  type        = map(string)
  default     = {}
}

variable "frontend_secret_env_vars" {
  description = "Secret environment variables for frontend service from Secret Manager"
  type = map(object({
    secret  = string
    version = string
  }))
  default = {}
}

variable "frontend_allow_public_access" {
  description = "Allow public access to frontend service"
  type        = bool
  default     = true
}

# Backend Service Variables
variable "backend_service_name" {
  description = "Name of the backend Cloud Run service"
  type        = string
  default     = "backend"
}

variable "backend_image" {
  description = "Container image for backend service"
  type        = string
}

variable "backend_port" {
  description = "Port the backend container listens on"
  type        = number
  default     = 8080
}

variable "backend_cpu" {
  description = "CPU allocation for backend (e.g., '1000m' for 1 vCPU)"
  type        = string
  default     = "1000m"
}

variable "backend_memory" {
  description = "Memory allocation for backend (e.g., '512Mi')"
  type        = string
  default     = "512Mi"
}

variable "backend_max_instances" {
  description = "Maximum number of backend instances"
  type        = number
  default     = 10
}

variable "backend_max_concurrency" {
  description = "Maximum concurrent requests per backend instance"
  type        = number
  default     = 80
}

variable "backend_health_check_path" {
  description = "Health check path for backend service"
  type        = string
  default     = "/health"
}

variable "backend_env_vars" {
  description = "Environment variables for backend service"
  type        = map(string)
  default     = {}
}

variable "backend_secret_env_vars" {
  description = "Secret environment variables for backend service from Secret Manager"
  type = map(object({
    secret  = string
    version = string
  }))
  default = {}
}

variable "backend_allow_public_access" {
  description = "Allow public access to backend service"
  type        = bool
  default     = true
}
