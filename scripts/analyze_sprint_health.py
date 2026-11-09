import pandas as pd
import json

df_sprints = pd.read_csv("data/raw/sprints.csv")
df_issues = pd.read_csv("data/raw/jira_issues.csv")
results = []

for _, sprint in df_sprints.iterrows():
    s_id = sprint["sprint_id"]
    s_issues = df_issues[df_issues["sprint_id"] == s_id]
    completed_pts = int(s_issues[s_issues["completed"] == 1]["story_points"].sum())
    committed_pts = int(sprint["committed_points"])
    crr = round((completed_pts / committed_pts) * 100, 2)
    added_pts = int(s_issues[s_issues["is_unplanned"] == 1]["story_points"].sum())
    svi = round((added_pts / committed_pts) * 100, 2)
    total_active_days = s_issues["total_cycle_days"].sum()
    friction_days = s_issues["review_days"].sum()
    friction_ratio = round(friction_days / total_active_days, 2) if total_active_days > 0 else 0
    spillover_issues = s_issues[s_issues["completed"] == 0]
    
    if svi > 20 or crr < 75 or friction_ratio > 0.35:
        risk_level = "High"
    elif svi > 12 or crr < 85:
        risk_level = "Medium"
    else:
        risk_level = "Low"
        
    results.append({
        "sprint_id": s_id,
        "sprint_name": sprint["sprint_name"],
        "squad": sprint["squad"],
        "committed_points": committed_pts,
        "added_points": added_pts,
        "completed_points": completed_pts,
        "crr_percentage": crr,
        "svi_percentage": svi,
        "review_friction_ratio": friction_ratio,
        "stalled_issue_count": len(spillover_issues),
        "stalled_points": int(spillover_issues["story_points"].sum()),
        "risk_level": risk_level,
        "spillover_keys": spillover_issues["issue_key"].tolist()
    })

with open("output/sprint_health_summary.json", "w") as f:
    json.dump(results, f, indent=2)
print("Sprint analytics computed and saved: output/sprint_health_summary.json")
