variable "resource_group_name" {
  type        = string
  description = "Name of resource group"
}

variable "location" {
  type        = string
  description = "Azure region"
}

variable "environment" {
  type        = string
  description = "Environment name"
}

variable "tags" {
  type        = map(string)
  default     = {}
  description = "Resource tags"
}
