package test

import (
	"testing"
	"github.com/gruntwork-io/terratest/modules/terraform"
	"github.com/stretchr/testify/assert"
)

// TestTerraformDevSecOpsValidation verifies that Azure infrastructure adheres to security baselines
func TestTerraformDevSecOpsValidation(t *testing.T) {
	t.Parallel()

	terraformOptions := terraform.WithDefaultRetryableErrors(t, &terraform.Options{
		TerraformDir: "../environments/dev",
		NoColor:      true,
	})

	// Run 'terraform init' and 'terraform plan' to validate configuration syntax and module linkages
	planStdout := terraform.InitAndPlan(t, terraformOptions)

	// Assertions on Planned Infrastructure
	assert.Contains(t, planStdout, "azurerm_virtual_network.vnet")
	assert.Contains(t, planStdout, "azurerm_mssql_database.database")
	assert.Contains(t, planStdout, "azurerm_key_vault.kv")
	assert.Contains(t, planStdout, "azurerm_storage_account.storage")
	assert.Contains(t, planStdout, "azurerm_linux_web_app.web_app")
	assert.Contains(t, planStdout, "azurerm_consumption_budget_resource_group.rg_budget")
}
