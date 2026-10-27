output "resource_group_name" {
  value       = azurerm_resource_group.rg.name
  description = "Production Resource Group Name"
}

output "application_url" {
  value       = module.compute.app_url
  description = "Production Public URL for Smart Accident Response System"
}

output "sql_server_fqdn" {
  value       = module.database.sql_server_fqdn
  description = "Production Azure SQL Server FQDN"
}

output "key_vault_uri" {
  value       = module.security_keyvault.key_vault_uri
  description = "Production Azure Key Vault URI"
}

output "storage_account_name" {
  value       = module.storage.storage_account_name
  description = "Production crash evidence storage account name"
}
