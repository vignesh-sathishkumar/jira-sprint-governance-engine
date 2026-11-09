import json

def run_ai_governance_audit():
    with open("output/sprint_health_summary.json", "r") as f:
        data = json.load(f)
        
    audit_reports = []
    for sp in data:
        crr = sp["crr_percentage"]
        svi = sp["svi_percentage"]
        friction = sp["review_friction_ratio"]
        risk = sp["risk_level"]
        stalled_pts = sp["stalled_points"]
        stalled_keys = sp["spillover_keys"]
        
        diagnosis = []
        recommendations = []
        if svi > 20:
            diagnosis.append(f"High scope volatility ({svi}% scope injected mid-sprint) eroded planned delivery buffers.")
            recommendations.append("Institute strict sprint scope freeze at Day 2. Require a 1-in-1-out trade-off policy.")
        if friction > 0.35:
            diagnosis.append(f"Code review friction ratio is high ({friction}), indicating severe pull request bottlenecks.")
            recommendations.append("Enforce a 24-hr PR review SLA or cap WIP (Work In Progress) per engineer.")
        if crr < 80:
            diagnosis.append(f"Commitment Reliability Ratio breached SLA floor at {crr}%. {stalled_pts} story points spilled over.")
            recommendations.append(f"Descope non-critical items: {', '.join(stalled_keys[:3])} to prioritize sprint goal completion.")
        if not diagnosis:
            diagnosis.append("Sprint execution on track with low scope variance and stable cycle times.")
            recommendations.append("Maintain existing velocity baseline and WIP limits.")
            
        audit_reports.append({
            "sprint_id": sp["sprint_id"],
            "sprint_name": sp["sprint_name"],
            "risk_assessment": risk,
            "delivery_confidence": "Low" if risk == "High" else ("Medium" if risk == "Medium" else "High"),
            "ai_root_cause_analysis": diagnosis,
            "actionable_descope_proposals": recommendations
        })
        
    with open("output/ai_governance_audit_report.json", "w") as f:
        json.dump(audit_reports, f, indent=2)
    print("AI Governance Audit completed: output/ai_governance_audit_report.json")

if __name__ == "__main__":
    run_ai_governance_audit()
