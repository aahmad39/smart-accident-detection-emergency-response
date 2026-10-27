# DevSecOps & Security Governance Guide

## Overview
Security in the **Smart Accident Detection & Emergency Response System** is integrated directly into every phase of the software delivery lifecycle (Shift-Left DevSecOps).

```
   +------------------+      +-------------------+      +------------------+      +-------------------+
   | Code & PR Review | ---> | Static Analysis   | ---> | IaC & Compliance | ---> | Deployment & Gate |
   | (Gitleaks, AI PR)|      | (Bandit, Flake8)  |      | (TFsec, Checkov) |      | (Terratest, OIDC) |
   +------------------+      +-------------------+      +------------------+      +-------------------+
```

---

## 1. Security Tools in CI/CD Pipeline

| Tool | Phase | Purpose | Policy / Threshold |
| :--- | :--- | :--- | :--- |
| **Gitleaks** | Pre-commit & CI | Secret scanning across git history | Fails build if any high-entropy key, token, or connection string is detected. |
| **TFLint** | IaC Linting | Validates Terraform syntax and Azure naming best practices | Fails build on unused variables or missing resource tags. |
| **TFsec** | IaC Security | Scans Terraform code for known security misconfigurations | Checks TLS configuration, unencrypted storage, and permissive NSG rules. |
| **Checkov** | IaC Compliance | Validates compliance against CIS Azure Foundation Benchmarks v2.0 | Verifies TDE on SQL, Soft-Delete on Key Vault, and HTTPS enforcement. |
| **Terratest** | Automated Validation | Programmatically plans and asserts cloud resource configurations | Go-based regression validation before applying infrastructure changes. |
| **Bandit** | App SAST | Static Application Security Testing for Python | Detects SQL injection, hardcoded passwords, unsafe deserialization. |
| **Safety / pip-audit** | Dependency SCA | Software Composition Analysis | Scans `requirements.txt` against CVE vulnerability databases. |

---

## 2. Policy as Code (Azure Policy)
Custom Azure Policy definitions in `devsecops/azure_policies/` enforce cloud governance:
- **`require_tagging.json`**: Denies creation of any resource lacking mandatory enterprise tags (`Environment`, `CostCenter`, `Owner`).
- **`restrict_public_access.json`**: Audits and restricts direct public network ingress on Azure Storage Accounts.

---

## 3. Secretless Cloud Authentication (OIDC & Managed Identity)
- **CI/CD to Azure:** GitHub Actions authenticates directly with Microsoft Entra ID using **OpenID Connect (OIDC) Federated Credentials**, eliminating the need for long-lived client secrets.
- **App Service to Azure SQL & Key Vault:** The Linux App Service uses a **User-Assigned Managed Identity (UAMI)**. All connection credentials are retrieved securely via Key Vault reference syntax:
  ```terraform
  "SECRET_KEY" = "@Microsoft.KeyVault(SecretUri=${module.security_keyvault.flask_secret_uri})"
  ```

---

## 4. Pre-Commit Hooks Setup for Developers
To enforce security rules before committing code locally:
```bash
pip install pre-commit
pre-commit install
pre-commit run --all-files
```
