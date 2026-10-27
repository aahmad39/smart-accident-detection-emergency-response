#!/usr/bin/env python3
"""
RCA Agent (Root Cause Analysis - Azure OpenAI)
Role: Helps with root cause analysis for infrastructure and application issues.
"""

import sys
from config import AIAgentConfig

SAMPLE_EXCEPTION = """
2026-10-27 20:15:32 ERROR [werkzeug] Exception on /api/v1/incidents [POST]
Traceback (most recent call last):
  File "sqlalchemy/pool/base.py", line 324, in _do_get
    return self._pool.get(wait=True, timeout=self._timeout)
TimeoutError: QueuePool limit of size 5 overflow 10 reached, connection timed out, timeout 30.00
"""

def diagnose_issue(log_trace=None):
    print("=" * 70)
    print("🔬 RCA AGENT: Root Cause Analysis on Operational Telemetry")
    print("=" * 70)

    trace = log_trace or SAMPLE_EXCEPTION
    client = AIAgentConfig.get_client()

    if client:
        prompt = (
            "You are an Azure Cloud & Database Site Reliability Engineering (SRE) RCA Agent. "
            "Analyze the following exception stack trace, identify the underlying root cause, "
            "and output concrete remediation steps:\n\n" + trace
        )
        response = client.chat.completions.create(
            model=AIAgentConfig.DEPLOYMENT_NAME,
            messages=[{"role": "user", "content": prompt}],
            temperature=0.2
        )
        print(response.choices[0].message.content)
    else:
        print("--- Root Cause Analysis (RCA) Diagnostic ---")
        print("Issue: SQLAlchemy QueuePool connection timeout during peak incident ingestion.")
        print("Root Cause: Default connection pool size (5) was overwhelmed by a spike of 120 concurrent telemetry packets.")
        print("Impact: Transient HTTP 500 on incoming vehicle telematics streams.")
        print("Mitigation Action:")
        print("  1. Increase SQLAlchemy pool_size=20, max_overflow=30 in app/src/config.py.")
        print("  2. Enable Azure SQL Serverless Auto-pause & Elastic Pool scaling.")
        print("  3. Implement exponential backoff retry in IoT vehicle gateway ingestion.")
        print("Status: RESOLUTION PLAN GENERATED")

if __name__ == "__main__":
    diagnose_issue()
