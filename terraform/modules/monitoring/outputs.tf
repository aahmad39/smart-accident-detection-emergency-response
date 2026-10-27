output "log_analytics_workspace_id" {
  value       = azurerm_log_analytics_workspace.law.id
  description = "Log Analytics Workspace ID"
}

output "app_insights_id" {
  value       = azurerm_application_insights.app_insights.id
  description = "Application Insights ID"
}

output "instrumentation_key" {
  value       = azurerm_application_insights.app_insights.instrumentation_key
  sensitive   = true
  description = "App Insights Instrumentation Key"
}

output "connection_string" {
  value       = azurerm_application_insights.app_insights.connection_string
  sensitive   = true
  description = "App Insights Connection String"
}
