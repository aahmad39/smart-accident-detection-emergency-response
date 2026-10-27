variable "resource_group_name" {
  type        = string
  description = "Resource Group Name"
}

variable "location" {
  type        = string
  description = "Azure region"
}

variable "sql_server_name" {
  type        = string
  description = "Globally unique SQL Server name"
}

variable "database_name" {
  type        = string
  default     = "hrdb"
  description = "Database name (hrdb matching architecture diagram)"
}

variable "administrator_login" {
  type        = string
  default     = "azureaccidentadmin"
  description = "SQL Server admin username"
}

variable "managed_identity_principal_id" {
  type        = string
  description = "Managed Identity principal for AAD admin"
}

variable "database_max_size_gb" {
  type        = number
  default     = 10
  description = "Max storage size for SQL database in GB"
}

variable "sku_name" {
  type        = string
  default     = "Basic"
  description = "SQL Database SKU (Basic for Dev, S1/S2/GP_Gen5_2 for Prod)"
}

variable "tags" {
  type        = map(string)
  default     = {}
  description = "Resource tags"
}
