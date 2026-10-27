variable "resource_group_name" {
  type        = string
  description = "Resource Group Name"
}

variable "location" {
  type        = string
  description = "Azure Region"
}

variable "storage_account_name" {
  type        = string
  description = "Globally unique storage account name"
}

variable "replication_type" {
  type        = string
  default     = "LRS"
  description = "Storage replication type (LRS, ZRS, GRS)"
}

variable "managed_identity_principal_id" {
  type        = string
  description = "Principal ID of Managed Identity"
}

variable "tags" {
  type        = map(string)
  default     = {}
  description = "Resource tags"
}
