output "app_service_id" {
  value       = azurerm_linux_web_app.web_app.id
  description = "Linux Web App Resource ID"
}

output "default_hostname" {
  value       = azurerm_linux_web_app.web_app.default_hostname
  description = "Default public URL of the application"
}

output "app_url" {
  value       = "https://${azurerm_linux_web_app.web_app.default_hostname}"
  description = "Full HTTPS application endpoint"
}
