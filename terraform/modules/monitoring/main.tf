# Monitoring Module: Azure Monitor & Application Insights
terraform {
  required_version = ">= 1.5.0"
  required_providers {
    azurerm = {
      source  = "hashicorp/azurerm"
      version = "~> 3.100"
    }
  }
}

resource "azurerm_log_analytics_workspace" "law" {
  name                = var.log_analytics_name
  location            = var.location
  resource_group_name = var.resource_group_name
  sku                 = "PerGB2018"
  retention_in_days   = 30
  tags                = var.tags
}

resource "azurerm_application_insights" "app_insights" {
  name                = var.app_insights_name
  location            = var.location
  resource_group_name = var.resource_group_name
  workspace_id        = azurerm_log_analytics_workspace.law.id
  application_type    = "web"
  tags                = var.tags
}

resource "azurerm_monitor_action_group" "critical_alert_group" {
  name                = "ag-accident-critical-${var.environment}"
  resource_group_name = var.resource_group_name
  short_name          = "AccidentOps"

  email_receiver {
    name          = "DevSecOpsLead"
    email_address = var.alert_email
  }

  tags = var.tags
}
