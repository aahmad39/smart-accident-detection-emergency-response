output "resource_group_name" {
  value       = azurerm_resource_group.rg.name
  description = "Resource Group Name"
}

output "application_url" {
  value       = module.compute.app_url
  description = "Public URL for Smart Accident Response System"
}

output "app_service_hostname" {
  value       = module.compute.default_hostname
  description = "App Service default hostname"
}

output "sql_server_fqdn" {
  value       = module.database.sql_server_fqdn
  description = "Azure SQL Server FQDN"
}

output "key_vault_uri" {
  value       = module.security_keyvault.key_vault_uri
  description = "Azure Key Vault URI"
}

output "storage_account_name" {
  value       = module.storage.storage_account_name
  description = "Crash evidence storage account name"
}

output "log_analytics_workspace_id" {
  value       = module.monitoring.log_analytics_workspace_id
  description = "Log Analytics Workspace ID"
}
