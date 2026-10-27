variable "project_name" {
  type        = string
  default     = "accident-uk"
  description = "Project name identifier"
}

variable "environment" {
  type        = string
  default     = "dev"
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
  default     = "super-secure-uk-emergency-dev-key-999-cad"
  description = "Secret key for session signing"
}

variable "tags" {
  type = map(string)
  default = {
    Owner       = "DevSecOps Engineering"
    CostCenter  = "UK-EMERGENCY-INFRA"
    Repository  = "smart-accident-detection-emergency-response"
  }
}
