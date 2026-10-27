variable "resource_group_name" {
  type        = string
  description = "Resource Group Name"
}

variable "location" {
  type        = string
  description = "Azure Region"
}

variable "environment" {
  type        = string
  description = "Environment name"
}

variable "app_service_plan_name" {
  type        = string
  description = "App Service Plan Name"
}

variable "app_service_name" {
  type        = string
  description = "Globally unique Linux Web App name"
}

variable "sku_name" {
  type        = string
  default     = "B1"
  description = "App Service SKU (B1 for dev, P1v3 for prod)"
}

variable "always_on" {
  type        = bool
  default     = false
  description = "Keep app loaded in memory"
}

variable "user_assigned_identity_id" {
  type        = string
  description = "User Assigned Managed Identity ID"
}

variable "user_assigned_identity_client_id" {
  type        = string
  description = "User Assigned Managed Identity Client ID"
}

variable "app_subnet_id" {
  type        = string
  description = "Subnet ID for regional VNet integration"
}

variable "app_insights_connection_string" {
  type        = string
  sensitive   = true
  description = "Application Insights connection string"
}

variable "storage_connection_string" {
  type        = string
  sensitive   = true
  description = "Storage account connection string"
}

variable "storage_container_name" {
  type        = string
  default     = "crash-evidence"
  description = "Storage blob container name"
}

variable "db_connection_string" {
  type        = string
  sensitive   = true
  description = "SQL Database connection string"
}

variable "flask_secret_uri" {
  type        = string
  description = "Key Vault Secret URI for Flask secret"
}

variable "tags" {
  type        = map(string)
  default     = {}
  description = "Resource tags"
}
