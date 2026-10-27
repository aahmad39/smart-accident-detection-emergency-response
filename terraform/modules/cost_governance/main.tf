# Cost Governance Module: Azure Cost Management Budget & Alerts
terraform {
  required_version = ">= 1.5.0"
  required_providers {
    azurerm = {
      source  = "hashicorp/azurerm"
      version = "~> 3.100"
    }
  }
}

resource "azurerm_consumption_budget_resource_group" "rg_budget" {
  name              = "budget-accident-${var.environment}"
  resource_group_id = var.resource_group_id
  amount            = var.budget_amount
  time_grain        = "Monthly"

  time_period {
    start_date = formatdate("YYYY-MM-01'T'00:00:00'Z'", timestamp())
  }

  # Warning threshold at 80%
  notification {
    enabled        = true
    threshold      = 80.0
    operator       = "GreaterThan"
    threshold_type = "Forecasted"

    contact_emails = [
      var.finops_contact_email
    ]
  }

  # Critical threshold at 100%
  notification {
    enabled        = true
    threshold      = 100.0
    operator       = "GreaterThan"
    threshold_type = "Actual"

    contact_emails = [
      var.finops_contact_email
    ]
  }

  lifecycle {
    ignore_changes = [
      time_period[0].start_date
    ]
  }
}
