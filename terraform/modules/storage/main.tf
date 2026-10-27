# Storage Module: Azure Blob Storage for Crash Evidence
terraform {
  required_version = ">= 1.5.0"
  required_providers {
    azurerm = {
      source  = "hashicorp/azurerm"
      version = "~> 3.100"
    }
  }
}

resource "azurerm_storage_account" "storage" {
  name                     = var.storage_account_name
  resource_group_name      = var.resource_group_name
  location                 = var.location
  account_tier             = "Standard"
  account_replication_type = var.replication_type
  min_tls_version          = "TLS1_2"
  enable_https_traffic_only = true

  blob_properties {
    delete_retention_policy {
      days = 14
    }
    container_delete_retention_policy {
      days = 14
    }
  }

  tags = var.tags
}

resource "azurerm_storage_container" "evidence_container" {
  name                  = "crash-evidence"
  storage_account_name  = azurerm_storage_account.storage.name
  container_access_type = "private"
}

resource "azurerm_storage_container" "dashcam_container" {
  name                  = "dashcam-footage"
  storage_account_name  = azurerm_storage_account.storage.name
  container_access_type = "private"
}

# Grant Managed Identity write access to crash evidence blobs
resource "azurerm_role_assignment" "storage_blob_contributor" {
  scope                = azurerm_storage_account.storage.id
  role_definition_name = "Storage Blob Data Contributor"
  principal_id         = var.managed_identity_principal_id
}
