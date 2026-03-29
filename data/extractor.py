import re
import pandas as pd
from config import COLUMN_PATTERNS
from data.utils import safe_float, safe_str


def normalize_column_name(name):
    s = str(name).lower().strip()
    s = re.sub(r"[^a-z0-9\s]", "", s)
    s = re.sub(r"\s+", " ", s)
    return s


def build_column_map(df):
    col_map = {}
    for col in df.columns:
        normalized = normalize_column_name(col)
        for field_key, patterns in COLUMN_PATTERNS.items():
            if field_key in col_map:
                continue
            for pattern in patterns:
                if pattern in normalized:
                    col_map[field_key] = col
                    break
    return col_map


def get_value(row, col_map, field, default=""):
    col_name = col_map.get(field, "")
    if not col_name:
        return default
    return row.get(col_name, default)


def find_project_rows(df, col_map):
    project_col = col_map.get("project_name", "")
    if not project_col:
        return []
    indices = []
    for i in range(len(df)):
        val = safe_str(df.iloc[i].get(project_col, ""))
        if val:
            indices.append(i)
    return indices


def parse_opening_date(raw_value):
    val = safe_str(raw_value)
    if not val:
        return "TBD", None
    if val.lower() == "opened":
        return "Opened", None
    try:
        parsed = pd.to_datetime(val, dayfirst=True)
        return parsed.strftime("%Y-%m-%d"), parsed
    except Exception:
        return val, None


def extract_concerns(df, col_map, start_row, end_row):
    concern_col = col_map.get("concerns", "")
    if not concern_col:
        return []
    concerns = []
    for i in range(start_row, end_row):
        val = safe_str(df.iloc[i].get(concern_col, ""))
        if val:
            concerns.append(val)
    return concerns


def extract_base_fields(row, col_map):
    data = {}
    data["project_name"] = safe_str(get_value(row, col_map, "project_name"))
    data["current_stage"] = safe_str(get_value(row, col_map, "current_stage"))
    data["currency"] = safe_str(get_value(row, col_map, "currency", "USD")) or "USD"
    data["proc_started"] = safe_str(get_value(row, col_map, "proc_started"))
    data["delivery_started"] = safe_str(get_value(row, col_map, "delivery_started"))

    date_str, date_parsed = parse_opening_date(get_value(row, col_map, "opening_date"))
    data["opening_date"] = date_str
    data["opening_date_parsed"] = date_parsed

    data["proposed_budget"] = safe_float(get_value(row, col_map, "proposed_budget", 0))
    data["client_budget"] = safe_float(get_value(row, col_map, "client_budget", 0))
    data["orders_placed"] = safe_float(get_value(row, col_map, "orders_placed", 0))
    data["orders_in_progress"] = safe_float(get_value(row, col_map, "orders_in_progress", 0))
    data["total_packages"] = safe_float(get_value(row, col_map, "total_packages", 0))
    data["packages_completed"] = safe_float(get_value(row, col_map, "packages_completed", 0))
    data["packages_in_progress"] = safe_float(get_value(row, col_map, "packages_in_progress", 0))
    data["total_pos"] = safe_float(get_value(row, col_map, "total_pos", 0))
    data["delivered_pos"] = safe_float(get_value(row, col_map, "delivered_pos", 0))

    overall_raw = safe_float(get_value(row, col_map, "overall_proc", 0))
    data["overall_proc_from_file"] = overall_raw * 100 if overall_raw <= 1 else overall_raw

    return data


def extract_projects_from_sheet(df):
    col_map = build_column_map(df)
    project_indices = find_project_rows(df, col_map)

    projects = []
    for idx, pi in enumerate(project_indices):
        row = df.iloc[pi]
        next_pi = project_indices[idx + 1] if idx + 1 < len(project_indices) else len(df)

        data = extract_base_fields(row, col_map)
        data["concerns"] = extract_concerns(df, col_map, pi, next_pi)
        projects.append(data)

    return projects
