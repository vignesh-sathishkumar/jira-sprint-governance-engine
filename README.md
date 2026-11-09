# Jira Sprint Health & AI Governance Engine

## Project Summary
A standalone Agile delivery intelligence pipeline that ingests sprint commitment records and Jira ticket transition histories, calculates core operational delivery KPIs (Commitment Reliability Ratio, Scope Volatility Index, and Review Friction Ratio), and applies a deterministic AI governance reasoning engine to detect delivery slippage and prescribe descope actions.

## Folder Contents
- `data/raw/sprints.csv`: 6 two-week sprint baselines across Core Platform and Checkout Experience squads.
- `data/raw/jira_issues.csv`: 500+ granular ticket records capturing issue types, story points, cycle times, and completion states.
- `output/sprint_health_summary.json`: Processed quantitative KPIs by sprint.
- `output/ai_governance_audit_report.json`: Formatted AI root-cause diagnoses and actionable trade-off recommendations.
- `scripts/`: Python execution scripts for data simulation, KPI aggregation, and AI auditing.

## Execution Order
```bash
pip install pandas numpy
python scripts/generate_sprint_data.py
python scripts/analyze_sprint_health.py
python scripts/ai_governance_agent.py
```
