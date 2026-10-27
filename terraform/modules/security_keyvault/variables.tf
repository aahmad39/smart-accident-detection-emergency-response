variable "resource_group_name" {
  type        = string
  description = "Resource Group Name"
}

variable "location" {
  type        = string
  description = "Azure Region"
}

variable "key_vault_name" {
  type        = string
  description = "Globally unique Key Vault name"
}

variable "managed_identity_principal_id" {
  type        = string
  description = "Principal ID of the Managed Identity needing read access"
}

variable "flask_secret_key" {
  type        = string
  sensitive   = true
  description = "Secret key for Flask session signing"
}

variable "db_connection_string" {
  type        = string
  sensitive   = true
  description = "Azure SQL connection string"
}

variable "tags" {
  type        = map(string)
  default     = {}
  description = "Resource tags"
}
