# Database Module: Azure SQL Server & Azure SQL Database (Tier 3)
terraform {
  required_version = ">= 1.5.0"
  required_providers {
    azurerm = {
      source  = "hashicorp/azurerm"
      version = "~> 3.100"
    }
    random = {
      source  = "hashicorp/random"
      version = "~> 3.6"
    }
  }
}

resource "random_password" "sql_admin_password" {
  length           = 24
  special          = true
  override_special = "!#$%&*()-_=+[]{}<>:?"
}

resource "azurerm_mssql_server" "sql_server" {
  name                         = var.sql_server_name
  resource_group_name          = var.resource_group_name
  location                     = var.location
  version                      = "12.0"
  administrator_login          = var.administrator_login
  administrator_login_password = random_password.sql_admin_password.result
  minimum_tls_version          = "1.2"

  # Azure Active Directory / Entra ID Admin
  azuread_administrator {
    login_username = "AAD-Admin"
    object_id      = var.managed_identity_principal_id
  }

  tags = var.tags
}

# Azure SQL Database (hrdb as specified in architecture)
resource "azurerm_mssql_database" "database" {
  name         = var.database_name
  server_id    = azurerm_mssql_server.sql_server.id
  collation    = "SQL_Latin1_General_CP1_CI_AS"
  license_type = "LicenseIncluded"
  max_size_gb  = var.database_max_size_gb
  sku_name     = var.sku_name

  tags = var.tags
}

# Allow Azure internal services to access SQL (firewall rule)
resource "azurerm_mssql_firewall_rule" "allow_azure_services" {
  name             = "AllowAzureServices"
  server_id        = azurerm_mssql_server.sql_server.id
  start_ip_address = "0.0.0.0"
  end_ip_address   = "0.0.0.0"
}
