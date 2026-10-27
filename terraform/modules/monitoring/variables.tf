variable "resource_group_name" {
  type        = string
  description = "Resource Group Name"
}

variable "location" {
  type        = string
  description = "Azure region"
}

variable "environment" {
  type        = string
  description = "Deployment environment"
}

variable "log_analytics_name" {
  type        = string
  description = "Log Analytics Workspace name"
}

variable "app_insights_name" {
  type        = string
  description = "Application Insights name"
}

variable "alert_email" {
  type        = string
  default     = "cloud-ops@emergency-response.uk"
  description = "Email for operational alerts"
}

variable "tags" {
  type        = map(string)
  default     = {}
  description = "Resource tags"
}
