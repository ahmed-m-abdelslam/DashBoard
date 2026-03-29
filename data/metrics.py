import pandas as pd
from config import CONCERN_KEYWORDS


def compute_basic_metrics(data):
    budget = data["client_budget"] if data["client_budget"] > 0 else data["proposed_budget"]
    data["effective_budget"] = budget
    data["packages_to_start"] = max(0, data["total_packages"] - data["packages_completed"] - data["packages_in_progress"])
    data["delivery_in_progress"] = max(0, data["total_pos"] - data["delivered_pos"])
    data["overall_completion"] = data["overall_proc_from_file"]
    data["pkg_completion_pct"] = (data["packages_completed"] / data["total_packages"] * 100) if data["total_packages"] > 0 else 0
    data["delivery_completion_pct"] = (data["delivered_pos"] / data["total_pos"] * 100) if data["total_pos"] > 0 else 0
    data["orders_placed_pct"] = (data["orders_placed"] / budget * 100) if budget > 0 else 0
    return data


def compute_budget_metrics(data):
    budget = data["effective_budget"]
    committed = data["orders_placed"] + data["orders_in_progress"]
    data["committed_spend"] = committed
    data["budget_utilization_pct"] = (committed / budget * 100) if budget > 0 else 0
    data["budget_variance"] = budget - committed
    data["budget_variance_pct"] = (data["budget_variance"] / budget * 100) if budget > 0 else 0
    data["savings_overrun"] = (budget - committed) if (budget > 0 and data["orders_placed"] > 0) else 0
    data["budget_uncommitted"] = max(0, budget - committed)

    if data["packages_completed"] > 0 and data["total_packages"] > 0:
        avg_cost = data["orders_placed"] / data["packages_completed"]
        remaining = data["total_packages"] - data["packages_completed"]
        data["projected_final_cost"] = data["orders_placed"] + data["orders_in_progress"] + (remaining * avg_cost * 0.7)
    else:
        data["projected_final_cost"] = committed

    data["projected_overrun"] = data["projected_final_cost"] - budget
    data["budget_at_risk"] = data["projected_final_cost"] > budget * 0.95
    return data


def compute_pipeline_metrics(data):
    initiated = data["packages_completed"] + data["packages_in_progress"]
    data["pipeline_initiation_rate"] = (initiated / data["total_packages"] * 100) if data["total_packages"] > 0 else 0
    data["pipeline_closure_rate"] = (data["packages_completed"] / initiated * 100) if initiated > 0 else 0
    data["ordering_completion_rate"] = data["pkg_completion_pct"]
    return data


def compute_delivery_metrics(data):
    data["po_delivery_rate"] = data["delivery_completion_pct"]
    data["outstanding_pos"] = max(0, data["total_pos"] - data["delivered_pos"])
    data["pos_per_package"] = (data["total_pos"] / data["packages_completed"]) if data["packages_completed"] > 0 else 0
    data["delivery_gap"] = data["overall_completion"] - data["po_delivery_rate"]
    return data


def compute_timeline_metrics(data):
    today = pd.Timestamp.now()
    parsed = data.get("opening_date_parsed")
    opening = data.get("opening_date", "TBD")

    if parsed:
        days_left = (parsed - today).days
        weeks_left = max(1, days_left / 7)
        data["days_to_opening"] = days_left
        data["delivery_pressure_index"] = data["outstanding_pos"] / weeks_left if days_left > 0 else 999
        remaining_pct = 100 - data["overall_completion"]
        data["required_daily_rate"] = remaining_pct / max(1, days_left) if days_left > 0 else 999

        if days_left < 0:
            data["urgency_category"] = "Overdue"
        elif days_left <= 90:
            data["urgency_category"] = "Imminent"
        elif days_left <= 180:
            data["urgency_category"] = "Near-term"
        elif days_left <= 365:
            data["urgency_category"] = "Medium-term"
        else:
            data["urgency_category"] = "Long-term"
    elif opening == "Opened":
        data["days_to_opening"] = 0
        data["delivery_pressure_index"] = 0
        data["required_daily_rate"] = 0
        data["urgency_category"] = "Opened"
    else:
        data["days_to_opening"] = None
        data["delivery_pressure_index"] = 0
        data["required_daily_rate"] = 0
        data["urgency_category"] = "TBD"
    return data


def compute_schedule_performance(data):
    parsed = data.get("opening_date_parsed")
    if parsed and data["overall_completion"] > 0:
        total_duration_est = 365
        days = data.get("days_to_opening", 365)
        elapsed_ratio = min(1.0, max(0.1, 1.0 - (days / total_duration_est)))
        expected = elapsed_ratio * 100
        data["schedule_performance_index"] = data["overall_completion"] / max(1, expected)
    else:
        data["schedule_performance_index"] = 1.0

    if data["overall_completion"] >= 75:
        data["completion_status"] = "On Track"
    elif data["overall_completion"] >= 40:
        data["completion_status"] = "Monitor"
    else:
        data["completion_status"] = "At Risk"
    return data


def categorize_concerns(data):
    concerns = data.get("concerns", [])
    text = " ".join(concerns).lower()
    categories = set()
    for category, keywords in CONCERN_KEYWORDS.items():
        if any(kw in text for kw in keywords):
            categories.add(category)
    data["concern_categories"] = list(categories)
    data["concern_count"] = len(concerns)
    data["concern_severity"] = len(categories)
    return data


def compute_risk_score(data):
    risk = 0
    opening = data.get("opening_date", "TBD")

    if data.get("opening_date_parsed"):
        days = data.get("days_to_opening", 999)
        completion = data["overall_completion"]
        if days < 0:
            risk += 15
        elif days < 90 and completion < 70:
            risk += 35
        elif days < 180 and completion < 40:
            risk += 25
        elif days < 90:
            risk += 15

    if data.get("budget_at_risk"):
        risk += 20
    if data.get("savings_overrun", 0) < 0:
        risk += 15

    dpi = data.get("delivery_pressure_index", 0)
    if dpi > 5:
        risk += 15
    elif dpi > 2:
        risk += 8

    total_pkg = data.get("total_packages", 0)
    to_start = data.get("packages_to_start", 0)
    if total_pkg > 0:
        ratio = to_start / total_pkg
        if ratio > 0.4:
            risk += 10
        elif ratio > 0.2:
            risk += 5

    if data["overall_completion"] < 20 and opening not in ("TBD", "Opened"):
        risk += 10

    data["risk_score"] = min(100, risk)
    data["schedule_risk"] = min(40, risk)
    data["budget_risk"] = 20 if data.get("budget_at_risk") else (15 if data.get("savings_overrun", 0) < 0 else 0)
    data["delivery_risk"] = min(15, dpi * 3)
    return data


def compute_all_metrics(data):
    data = compute_basic_metrics(data)
    data = compute_budget_metrics(data)
    data = compute_pipeline_metrics(data)
    data = compute_delivery_metrics(data)
    data = compute_timeline_metrics(data)
    data = compute_schedule_performance(data)
    data = categorize_concerns(data)
    data = compute_risk_score(data)
    return data
