# Identity Module: User Assigned Managed Identity
terraform {
  required_version = ">= 1.5.0"
  required_providers {
    azurerm = {
      source  = "hashicorp/azurerm"
      version = "~> 3.100"
    }
  }
}

resource "azurerm_user_assigned_identity" "app_identity" {
  name                = "uami-accident-${var.environment}"
  resource_group_name = var.resource_group_name
  location            = var.location
  tags                = var.tags
}
