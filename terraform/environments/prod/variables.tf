variable "project_name" {
  type        = string
  default     = "accident-uk"
  description = "Project name identifier"
}

variable "environment" {
  type        = string
  default     = "prod"
  description = "Deployment environment"
}

variable "location" {
  type        = string
  default     = "uksouth"
  description = "Primary Azure region (UK South)"
}

variable "flask_secret_key" {
  type        = string
  sensitive   = true
  description = "Production secret key for session signing"
}

variable "tags" {
  type = map(string)
  default = {
    Owner       = "Emergency Services Dispatch Command"
    CostCenter  = "UK-999-NATIONAL-INFRA"
    Repository  = "smart-accident-detection-emergency-response"
  }
}
