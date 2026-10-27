variable "resource_group_id" {
  type        = string
  description = "Target Resource Group ID"
}

variable "environment" {
  type        = string
  description = "Deployment environment"
}

variable "budget_amount" {
  type        = number
  default     = 250
  description = "Monthly budget amount in GBP / USD"
}

variable "finops_contact_email" {
  type        = string
  default     = "finops@emergency-response.uk"
  description = "FinOps lead contact email for budget alerts"
}
