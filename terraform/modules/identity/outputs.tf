output "identity_id" {
  value       = azurerm_user_assigned_identity.app_identity.id
  description = "User Assigned Identity resource ID"
}

output "principal_id" {
  value       = azurerm_user_assigned_identity.app_identity.principal_id
  description = "Principal ID of Managed Identity"
}

output "client_id" {
  value       = azurerm_user_assigned_identity.app_identity.client_id
  description = "Client ID of Managed Identity"
}
