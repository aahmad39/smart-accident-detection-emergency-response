# Compute Module: Azure App Service (Linux Web App for Flask)
terraform {
  required_version = ">= 1.5.0"
  required_providers {
    azurerm = {
      source  = "hashicorp/azurerm"
      version = "~> 3.100"
    }
  }
}

resource "azurerm_service_plan" "app_plan" {
  name                = var.app_service_plan_name
  location            = var.location
  resource_group_name = var.resource_group_name
  os_type             = "Linux"
  sku_name            = var.sku_name
  tags                = var.tags
}

resource "azurerm_linux_web_app" "web_app" {
  name                = var.app_service_name
  location            = var.location
  resource_group_name = var.resource_group_name
  service_plan_id     = azurerm_service_plan.app_plan.id
  https_only          = true

  identity {
    type         = "UserAssigned"
    identity_ids = [var.user_assigned_identity_id]
  }

  site_config {
    always_on        = var.always_on
    minimum_tls_version = "1.2"
    ftps_state       = "Disabled"
    health_check_path = "/api/v1/health"

    application_stack {
      python_version = "3.11"
    }
  }

  app_settings = {
    "FLASK_ENV"                            = var.environment
    "PORT"                                 = "8000"
    "APPLICATIONINSIGHTS_CONNECTION_STRING"= var.app_insights_connection_string
    "AZURE_STORAGE_CONTAINER_NAME"         = var.storage_container_name
    "AZURE_STORAGE_CONNECTION_STRING"      = var.storage_connection_string
    "AZURE_SQL_CONNECTION_STRING"          = var.db_connection_string
    "SECRET_KEY"                           = "@Microsoft.KeyVault(SecretUri=${var.flask_secret_uri})"
    "AZURE_CLIENT_ID"                      = var.user_assigned_identity_client_id
  }

  # Regional VNet Integration for Secure Private Egress
  virtual_network_subnet_id = var.app_subnet_id

  tags = var.tags
}
