output "budget_id" {
  value       = azurerm_consumption_budget_resource_group.rg_budget.id
  description = "Consumption budget ID"
}
