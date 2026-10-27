# Azure OpenAI AI Agents Architecture & Operational Guide

## Overview
This platform utilizes a multi-agent framework powered by **Azure OpenAI Service (GPT-4o)** to automate complex cloud engineering, security analysis, code reviews, and live diagnostic workflows.

```
       +------------------------------------------------------------+
       |             Azure OpenAI (GPT-4o Deployment)               |
       +------------------------------------------------------------+
             |                 |                 |            |
             v                 v                 v            v
     +--------------+  +---------------+  +-----------+  +------------+
     |  Risk Agent  |  |Security Agent |  |PR Review  |  |Post-Deploy |
     |  (IaC & Arch)|  |(Vuln & Miscon)|  |Agent (PRs)|  |Validation  |
     +--------------+  +---------------+  +-----------+  +------------+
                                                              |
                                                              v
                                                       +------------+
                                                       | RCA Agent  |
                                                       | (Errors)   |
                                                       +------------+
```

---

## 1. AI Agent Directory & Roles

### 1. Risk Agent (`ai_agents/risk_agent.py`)
- **Role:** Identifies architectural risks, single points of failure (SPOFs), and cost optimization opportunities in Terraform templates and architecture.
- **Workflow:** Ingests `.tf` configuration files, compares resource specifications with the Azure Well-Architected Framework, and emits prioritized severity ratings and mitigations.

### 2. Security Agent (`ai_agents/security_agent.py`)
- **Role:** Detects configuration misconfigurations, excessive permissions, and compliance breaches.
- **Workflow:** Inspects network security groups, firewall rules, and encryption parameters against CIS Azure Benchmarks v2.0.

### 3. PR Review Agent (`ai_agents/pr_review_agent.py`)
- **Role:** Autonomous GitHub Pull Request Reviewer.
- **Workflow:** Runs in `.github/workflows/ai-pr-reviewer.yml` upon every PR update. It fetches `git diff`, validates PEP8 style, identifies anti-patterns, and writes comments directly to the pull request.

### 4. Post-Deployment Validation Agent (`ai_agents/post_deploy_agent.py`)
- **Role:** Performs automated end-to-end cloud infrastructure verification after deployment.
- **Workflow:** Probes `/api/v1/health`, verifies latency thresholds, and asserts connectivity to Azure SQL (`hrdb`), Key Vault, and Blob Storage.

### 5. RCA Agent (`ai_agents/rca_agent.py`)
- **Role:** Root Cause Analysis assistant for operational telemetry and error traces.
- **Workflow:** Accepts raw application crash logs, identifies the underlying fault (e.g., connection pool exhaustion or network socket timeouts), and outputs immediate remediation actions.

---

## 2. Invoking AI Agents via UI and CLI

### Web Dashboard
Navigate to `http://localhost:5000/ai-hub` to execute any of the 5 agents interactively with live telemetry and code snippets.

### Command Line Execution
```bash
# Analyze Terraform IaC for architectural risks
python ai_agents/risk_agent.py

# Audit Cloud Security Posture
python ai_agents/security_agent.py

# Review PR Code Diffs
python ai_agents/pr_review_agent.py

# Validate Post-Deployment Cloud State
python ai_agents/post_deploy_agent.py

# Run Root Cause Analysis on an Error Trace
python ai_agents/rca_agent.py
```
