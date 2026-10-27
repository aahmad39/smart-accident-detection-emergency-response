# Security Module: Azure Key Vault & Secrets
terraform {
  required_version = ">= 1.5.0"
  required_providers {
    azurerm = {
      source  = "hashicorp/azurerm"
      version = "~> 3.100"
    }
  }
}

data "azurerm_client_config" "current" {}

resource "azurerm_key_vault" "kv" {
  name                       = var.key_vault_name
  location                   = var.location
  resource_group_name        = var.resource_group_name
  tenant_id                  = data.azurerm_client_config.current.tenant_id
  sku_name                   = "standard"
  soft_delete_retention_days = 90
  purge_protection_enabled   = true
  enable_rbac_authorization  = true

  network_acls {
    bypass         = "AzureServices"
    default_action = "Allow"
  }

  tags = var.tags
}

# Assign Key Vault Secrets User role to Managed Identity
resource "azurerm_role_assignment" "uami_kv_secrets_user" {
  scope                = azurerm_key_vault.kv.id
  role_definition_name = "Key Vault Secrets User"
  principal_id         = var.managed_identity_principal_id
}

# Current user/deployer role assignment to manage secrets in CI/CD
resource "azurerm_role_assignment" "deployer_kv_officer" {
  scope                = azurerm_key_vault.kv.id
  role_definition_name = "Key Vault Secrets Officer"
  principal_id         = data.azurerm_client_config.current.object_id
}

# Secret: Flask Application Secret Key
resource "azurerm_key_vault_secret" "flask_secret" {
  name         = "flask-secret-key"
  value        = var.flask_secret_key
  key_vault_id = azurerm_key_vault.kv.id
  depends_on   = [azurerm_role_assignment.deployer_kv_officer]
}

# Secret: SQL DB Connection String
resource "azurerm_key_vault_secret" "db_conn_str" {
  name         = "sql-connection-string"
  value        = var.db_connection_string
  key_vault_id = azurerm_key_vault.kv.id
  depends_on   = [azurerm_role_assignment.deployer_kv_officer]
}
