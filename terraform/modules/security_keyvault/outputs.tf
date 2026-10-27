output "key_vault_id" {
  value       = azurerm_key_vault.kv.id
  description = "Key Vault Resource ID"
}

output "key_vault_uri" {
  value       = azurerm_key_vault.kv.vault_uri
  description = "Key Vault URI"
}

output "flask_secret_uri" {
  value       = azurerm_key_vault_secret.flask_secret.versionless_id
  description = "Key Vault Secret ID for Flask"
}

output "db_conn_str_uri" {
  value       = azurerm_key_vault_secret.db_conn_str.versionless_id
  description = "Key Vault Secret ID for SQL Connection"
}
