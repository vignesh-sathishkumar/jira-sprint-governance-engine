import pandas as pd
import numpy as np
from datetime import datetime, timedelta

np.random.seed(20261107)
squads = ["Core Platform", "Checkout Experience"]
sprint_count = 6
sprints = []
issues = []
issue_counter = 1000
base_start = datetime(2026, 1, 5)

for s in range(1, sprint_count + 1):
    sprint_start = base_start + timedelta(days=(s - 1) * 14)
    sprint_end = sprint_start + timedelta(days=13)
    for squad in squads:
        sprint_id = f"SP-{squad[:4].upper()}-S{s}"
        committed_points = int(np.random.randint(65, 95))
        creep_factor = 0.30 if s in [4, 5] else 0.08
        added_points = int(committed_points * creep_factor)
        
        sprints.append({
            "sprint_id": sprint_id,
            "sprint_name": f"{squad} - Sprint {s}",
            "squad": squad,
            "start_date": sprint_start.strftime("%Y-%m-%d"),
            "end_date": sprint_end.strftime("%Y-%m-%d"),
            "committed_points": committed_points,
            "added_points": added_points,
            "total_scope_points": committed_points + added_points
        })
        
        current_points = 0
        target_points = committed_points + added_points
        while current_points < target_points:
            issue_counter += 1
            key = f"ENG-{issue_counter}"
            issue_type = str(np.random.choice(["Story", "Bug", "Task"], p=[0.65, 0.25, 0.10]))
            points = int(np.random.choice([1, 2, 3, 5, 8], p=[0.15, 0.25, 0.35, 0.15, 0.10]))
            is_unplanned = 1 if current_points >= committed_points else 0
            added_on_day = int(np.random.randint(2, 10)) if is_unplanned else 0
            dev_days = float(np.random.uniform(1.5, 4.0))
            review_friction = 3.5 if s in [4, 5] and issue_type == "Story" else 0.8
            review_days = float(np.random.uniform(0.5, 1.5)) + review_friction
            qa_days = float(np.random.uniform(0.5, 2.0))
            total_cycle_time = dev_days + review_days + qa_days
            
            if total_cycle_time + added_on_day > 12:
                status = str(np.random.choice(["In Code Review", "In QA", "Blocked"], p=[0.5, 0.3, 0.2]))
                completed = 0
            else:
                status = "Done"
                completed = 1
                
            issues.append({
                "issue_key": key,
                "sprint_id": sprint_id,
                "squad": squad,
                "issue_type": issue_type,
                "story_points": points,
                "is_unplanned": is_unplanned,
                "added_on_day": added_on_day,
                "status": status,
                "completed": completed,
                "dev_days": round(dev_days, 1),
                "review_days": round(review_days, 1),
                "qa_days": round(qa_days, 1),
                "total_cycle_days": round(total_cycle_time, 1)
            })
            current_points += points

pd.DataFrame(sprints).to_csv("data/raw/sprints.csv", index=False)
pd.DataFrame(issues).to_csv("data/raw/jira_issues.csv", index=False)
print("Data generation complete: data/raw/sprints.csv and data/raw/jira_issues.csv updated.")
