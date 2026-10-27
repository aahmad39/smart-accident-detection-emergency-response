output "storage_account_id" {
  value       = azurerm_storage_account.storage.id
  description = "Storage Account ID"
}

output "storage_account_name" {
  value       = azurerm_storage_account.storage.name
  description = "Storage Account Name"
}

output "primary_blob_endpoint" {
  value       = azurerm_storage_account.storage.primary_blob_endpoint
  description = "Primary Blob Endpoint"
}

output "evidence_container_name" {
  value       = azurerm_storage_container.evidence_container.name
  description = "Evidence container name"
}

output "primary_connection_string" {
  value       = azurerm_storage_account.storage.primary_connection_string
  sensitive   = true
  description = "Storage account connection string"
}
