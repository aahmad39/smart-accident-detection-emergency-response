# Environment: DEV (Smart Accident Detection & Emergency Response System)
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

  # Azure Blob Storage backend for state locking (configured via CI/CD)
  # backend "azurerm" {}
}

provider "azurerm" {
  features {
    key_vault {
      purge_soft_delete_on_destroy    = false
      recover_soft_deleted_key_vaults = true
    }
  }
}

# Unique suffix generator to prevent global Azure naming collisions
resource "random_string" "suffix" {
  length  = 5
  special = false
  upper   = false
}

# Core Resource Group
resource "azurerm_resource_group" "rg" {
  name     = "rg-${var.project_name}-${var.environment}-${var.location}"
  location = var.location
  tags     = local.common_tags
}

locals {
  common_tags = merge(var.tags, {
    Environment = var.environment
    Project     = var.project_name
    ManagedBy   = "Terraform"
    Security    = "DevSecOps-Automated"
    FinOps      = "Optimized"
  })
}

# 1. Identity Module
module "identity" {
  source              = "../../modules/identity"
  resource_group_name = azurerm_resource_group.rg.name
  location            = var.location
  environment         = var.environment
  tags                = local.common_tags
}

# 2. Networking Module
module "networking" {
  source              = "../../modules/networking"
  resource_group_name = azurerm_resource_group.rg.name
  location            = var.location
  environment         = var.environment
  vnet_name           = "vnet-${var.project_name}-${var.environment}"
  tags                = local.common_tags
}

# 3. Monitoring Module (Log Analytics & Application Insights)
module "monitoring" {
  source              = "../../modules/monitoring"
  resource_group_name = azurerm_resource_group.rg.name
  location            = var.location
  environment         = var.environment
  log_analytics_name  = "log-${var.project_name}-${var.environment}-${random_string.suffix.result}"
  app_insights_name   = "appi-${var.project_name}-${var.environment}-${random_string.suffix.result}"
  tags                = local.common_tags
}

# 4. Storage Module (Azure Blob Storage for Crash Evidence)
module "storage" {
  source                        = "../../modules/storage"
  resource_group_name           = azurerm_resource_group.rg.name
  location                      = var.location
  storage_account_name          = "st${replace(var.project_name, "-", "")}${var.environment}${random_string.suffix.result}"
  replication_type              = "LRS"
  managed_identity_principal_id = module.identity.principal_id
  tags                          = local.common_tags
}

# 5. Database Module (Azure SQL Server & Database 'hrdb')
module "database" {
  source                        = "../../modules/database"
  resource_group_name           = azurerm_resource_group.rg.name
  location                      = var.location
  sql_server_name               = "sql-${var.project_name}-${var.environment}-${random_string.suffix.result}"
  database_name                 = "hrdb"
  sku_name                      = "Basic"
  managed_identity_principal_id = module.identity.principal_id
  tags                          = local.common_tags
}

# 6. Key Vault Module
module "security_keyvault" {
  source                        = "../../modules/security_keyvault"
  resource_group_name           = azurerm_resource_group.rg.name
  location                      = var.location
  key_vault_name                = "kv-${var.project_name}-${var.environment}-${random_string.suffix.result}"
  managed_identity_principal_id = module.identity.principal_id
  flask_secret_key              = var.flask_secret_key
  db_connection_string          = module.database.connection_string
  tags                          = local.common_tags
}

# 7. Compute Module (Azure App Service for Flask Web App)
module "compute" {
  source                           = "../../modules/compute_appservice"
  resource_group_name              = azurerm_resource_group.rg.name
  location                         = var.location
  environment                      = var.environment
  app_service_plan_name            = "asp-${var.project_name}-${var.environment}"
  app_service_name                 = "app-${var.project_name}-${var.environment}-${random_string.suffix.result}"
  sku_name                         = "B1"
  always_on                        = false
  user_assigned_identity_id        = module.identity.identity_id
  user_assigned_identity_client_id = module.identity.client_id
  app_subnet_id                    = module.networking.app_subnet_id
  app_insights_connection_string   = module.monitoring.connection_string
  storage_connection_string        = module.storage.primary_connection_string
  storage_container_name           = module.storage.evidence_container_name
  db_connection_string             = module.database.connection_string
  flask_secret_uri                 = module.security_keyvault.flask_secret_uri
  tags                             = local.common_tags
}

# 8. Cost Governance Module (FinOps Budget & Threshold Alerts)
module "cost_governance" {
  source               = "../../modules/cost_governance"
  resource_group_id    = azurerm_resource_group.rg.id
  environment          = var.environment
  budget_amount        = 100
  finops_contact_email = "finops-dev@emergency-response.uk"
}
