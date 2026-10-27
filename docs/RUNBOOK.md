# Operational Runbook: Local Setup & Azure Deployment

## 1. Quickstart: Running Locally

### Step 1: Clone & Setup Environment
```bash
git clone https://github.com/<your-username>/smart-accident-detection-emergency-response.git
cd smart-accident-detection-emergency-response
```

### Step 2: Install Python Dependencies
```bash
# Using Python 3.11+
python -m venv venv
# Windows:
venv\Scripts\activate
# Linux/macOS:
source venv/bin/activate

pip install -r app/requirements.txt
```

### Step 3: Configure Environment Variables
Copy `.env.example` to `.env`:
```bash
cp .env.example .env
```

### Step 4: Launch the Monolithic Application
```bash
cd app
python run.py
```
Open your browser to:
👉 **`http://localhost:5000`**

The system automatically initializes and seeds the local database with realistic UK emergency responders, vehicles, and active incidents.

---

## 2. Deploying to Azure using Terraform

### Prerequisites
- [Azure CLI](https://learn.microsoft.com/en-us/cli/azure/install-azure-cli) logged in (`az login`)
- [Terraform >= 1.5.0](https://www.terraform.io/downloads.html)

### Step 1: Select Environment
```bash
cd terraform/environments/dev
```

### Step 2: Initialize & Apply
```bash
# Initialize Terraform providers and modules
terraform init

# Review planned Azure resources
terraform plan

# Deploy infrastructure to Azure UK South
terraform apply
```

Outputs will display:
- `application_url`: The HTTPS endpoint of your deployed App Service
- `sql_server_fqdn`: The fully qualified domain name of Azure SQL
- `key_vault_uri`: The Azure Key Vault secret storage URI

---

## 3. GitHub Actions CI/CD Pipeline Configuration

To enable automated CI/CD deployments from GitHub Actions, configure the following GitHub Repository Secrets under **Settings > Secrets and variables > Actions**:

| Secret Name | Description |
| :--- | :--- |
| `AZURE_CLIENT_ID` | Managed Identity / App Registration Client ID |
| `AZURE_TENANT_ID` | Microsoft Entra Tenant ID |
| `AZURE_SUBSCRIPTION_ID` | Target Azure Subscription ID |
| `AZURE_APP_NAME` | Name of Azure App Service (e.g. `app-accident-uk-dev`) |
| `AZURE_OPENAI_ENDPOINT` | Azure OpenAI Resource Endpoint URL |
| `AZURE_OPENAI_API_KEY` | Azure OpenAI Secret Key |

---

## 4. Running Verification & Unit Tests
```bash
cd app
pytest tests/ -v
```

To run security scans:
```bash
bandit -r src/
```
