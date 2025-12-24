# Cloud Run Terraform Deployment

This directory contains Terraform configuration for deploying frontend and backend services to Google Cloud Run with automatic scaling and Secret Manager integration.

## Features

- ✅ **Auto-scaling**: Services scale to 0 instances after 5 minutes of no traffic (cost optimization)
- ✅ **HTTPS Access**: Both services are accessible via HTTPS endpoints
- ✅ **Secret Management**: Environment variables injected from Google Secret Manager
- ✅ **Least-Privilege IAM**: Dedicated service accounts with minimal required permissions
- ✅ **Cold Start Optimization**: Configured for cold start time < 5s with startup CPU boost
- ✅ **Health Checks**: Startup and liveness probes for reliability

## Prerequisites

1. **Terraform**: Version 1.5.0 or higher
   ```bash
   terraform version
   ```

2. **GCP Project**: A Google Cloud Platform project with billing enabled

3. **Required APIs**: Enable the following APIs in your GCP project:
   ```bash
   gcloud services enable run.googleapis.com
   gcloud services enable secretmanager.googleapis.com
   gcloud services enable iam.googleapis.com
   ```

4. **GCP Authentication**: Set up authentication
   ```bash
   gcloud auth application-default login
   ```

5. **Container Images**: Build and push your frontend and backend images to GCR or Artifact Registry
   ```bash
   # Example for GCR
   docker build -t gcr.io/YOUR-PROJECT-ID/frontend:latest ./frontend
   docker push gcr.io/YOUR-PROJECT-ID/frontend:latest
   
   docker build -t gcr.io/YOUR-PROJECT-ID/backend:latest ./backend
   docker push gcr.io/YOUR-PROJECT-ID/backend:latest
   ```

## Quick Start

1. **Copy the example variables file**:
   ```bash
   cp terraform.tfvars.example terraform.tfvars
   ```

2. **Edit terraform.tfvars** with your values:
   ```hcl
   project_id = "your-gcp-project-id"
   frontend_image = "gcr.io/your-project-id/frontend:latest"
   backend_image = "gcr.io/your-project-id/backend:latest"
   ```

3. **Initialize Terraform**:
   ```bash
   terraform init
   ```

4. **Review the plan**:
   ```bash
   terraform plan
   ```

5. **Apply the configuration**:
   ```bash
   terraform apply
   ```

6. **Get the service URLs**:
   ```bash
   terraform output frontend_url
   terraform output backend_url
   ```

## Configuration

### Auto-Scaling

Services are configured to scale to zero when idle:
- `min_instance_count = 0` - Scales down to 0 instances
- `max_instance_count` - Configurable per service (default: 10)

Cloud Run automatically scales down instances to zero when there is no traffic. The scale-down typically occurs after approximately 15 minutes of inactivity, though this may vary. Setting `min_instance_count = 0` enables this cost-saving behavior.

### Secret Manager Integration

To use secrets from Google Secret Manager:

1. **Create secrets** in Secret Manager:
   ```bash
   echo -n "your-secret-value" | gcloud secrets create my-secret --data-file=-
   ```

2. **Configure in terraform.tfvars**:
   ```hcl
   backend_secret_env_vars = {
     "DATABASE_PASSWORD" = {
       secret  = "database-password"
       version = "latest"
     }
   }
   ```

The service accounts are automatically granted `secretmanager.secretAccessor` role.

### IAM and Security

Each service has its own dedicated service account with least-privilege permissions:
- `frontend-cloudrun-sa`: Service account for frontend
- `backend-cloudrun-sa`: Service account for backend

Both service accounts have:
- `roles/secretmanager.secretAccessor` - To read secrets (only if configured)
- `roles/run.invoker` - Granted to `allUsers` for public access (configurable)

To restrict access, set `frontend_allow_public_access = false` or `backend_allow_public_access = false`.

### Cold Start Optimization

The configuration includes several optimizations for fast cold starts:
- `cpu_idle = true` - CPU always allocated
- `startup_cpu_boost = true` - Extra CPU during startup
- Optimized health check configuration
- `startup_probe` with fast initial checks (3s intervals)

These settings ensure cold start times remain under 5 seconds.

## Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `project_id` | GCP Project ID | Required |
| `region` | GCP region | `us-central1` |
| `frontend_service_name` | Frontend service name | `frontend` |
| `frontend_image` | Frontend container image | Required |
| `frontend_port` | Frontend container port | `8080` |
| `frontend_cpu` | Frontend CPU allocation | `1000m` |
| `frontend_memory` | Frontend memory allocation | `512Mi` |
| `frontend_max_instances` | Max frontend instances | `10` |
| `backend_service_name` | Backend service name | `backend` |
| `backend_image` | Backend container image | Required |
| `backend_port` | Backend container port | `8080` |
| `backend_cpu` | Backend CPU allocation | `1000m` |
| `backend_memory` | Backend memory allocation | `512Mi` |
| `backend_max_instances` | Max backend instances | `10` |

See `variables.tf` for the complete list of variables.

## Outputs

After applying, Terraform will output:
- `frontend_url` - HTTPS URL of the frontend service
- `backend_url` - HTTPS URL of the backend service
- `frontend_service_account_email` - Email of frontend service account
- `backend_service_account_email` - Email of backend service account

## Maintenance

### Update Service

To update a service with a new image:

1. Update the image variable in `terraform.tfvars`
2. Run `terraform apply`

### View Logs

```bash
gcloud run services logs read frontend --region=us-central1
gcloud run services logs read backend --region=us-central1
```

### Monitor Scaling

View service details including current instance count:
```bash
gcloud run services describe frontend --region=us-central1
gcloud run services describe backend --region=us-central1
```

## Cleanup

To destroy all resources:
```bash
terraform destroy
```

## Troubleshooting

### Permission Denied

Ensure your GCP account has the necessary permissions:
- `roles/run.admin`
- `roles/iam.serviceAccountAdmin`
- `roles/secretmanager.admin` (if using secrets)

### Cold Start Issues

If cold starts are taking longer than 5 seconds:
1. Optimize your application startup time
2. Consider increasing `frontend_cpu` or `backend_cpu`
3. Review startup probe configuration
4. Use minimum instances (`min_instance_count = 1`) if cold starts are critical

### Cost Optimization

To minimize costs:
- Keep `min_instance_count = 0` (default)
- Set appropriate `max_instance_count` limits
- Use smaller CPU/memory allocations if possible
- Monitor usage with GCP Cost Explorer

## Architecture

```
┌─────────────────┐         ┌─────────────────┐
│   Frontend      │         │    Backend      │
│  Cloud Run      │────────▶│   Cloud Run     │
│                 │         │                 │
│ Min: 0          │         │ Min: 0          │
│ Max: 10         │         │ Max: 10         │
└────────┬────────┘         └────────┬────────┘
         │                           │
         │                           │
         ▼                           ▼
┌─────────────────────────────────────────────┐
│         Google Secret Manager               │
│  • Database credentials                     │
│  • API keys                                 │
│  • JWT secrets                              │
└─────────────────────────────────────────────┘
```

## License

This Terraform configuration is provided as-is for the fayzy project.
