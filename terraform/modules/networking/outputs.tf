output "vnet_id" {
  value       = azurerm_virtual_network.vnet.id
  description = "Virtual Network ID"
}

output "vnet_name" {
  value       = azurerm_virtual_network.vnet.name
  description = "Virtual Network Name"
}

output "app_subnet_id" {
  value       = azurerm_subnet.app_subnet.id
  description = "App Service delegation subnet ID"
}

output "db_subnet_id" {
  value       = azurerm_subnet.db_subnet.id
  description = "Database subnet ID"
}

output "pe_subnet_id" {
  value       = azurerm_subnet.pe_subnet.id
  description = "Private Endpoints subnet ID"
}
