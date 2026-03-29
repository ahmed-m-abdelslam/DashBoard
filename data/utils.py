import pandas as pd


def safe_float(val):
    try:
        v = float(val)
        return 0.0 if pd.isna(v) else v
    except (ValueError, TypeError):
        return 0.0


def safe_str(val):
    s = str(val).strip()
    return "" if s.lower() in ("nan", "nat", "none", "") else s


def hex_to_rgba(hex_color, alpha=1.0):
    hex_color = hex_color.lstrip("#")
    r = int(hex_color[0:2], 16)
    g = int(hex_color[2:4], 16)
    b = int(hex_color[4:6], 16)
    return f"rgba({r},{g},{b},{alpha})"


def fmt_num(val, currency=""):
    prefix = f"{currency} " if currency else ""
    if abs(val) >= 1_000_000:
        return f"{prefix}{val / 1_000_000:,.2f}M"
    elif abs(val) >= 1_000:
        return f"{prefix}{val / 1_000:,.1f}K"
    return f"{prefix}{val:,.0f}"


def status_color(pct):
    from config import THEME
    if pct >= 75:
        return THEME["success"]
    elif pct >= 40:
        return THEME["warning"]
    return THEME["danger"]


def risk_color(score):
    from config import THEME
    if score >= 60:
        return THEME["danger"]
    elif score >= 30:
        return THEME["warning"]
    return THEME["success"]


def risk_label(score):
    if score >= 60:
        return "High Risk"
    elif score >= 30:
        return "Medium"
    return "Low Risk"


def urgency_color(category):
    from config import THEME
    mapping = {
        "Overdue": THEME["danger"],
        "Imminent": THEME["orange"],
        "Near-term": THEME["warning"],
        "Medium-term": THEME["info"],
        "Long-term": THEME["success"],
        "Opened": THEME["purple"],
        "TBD": THEME["text_muted"],
    }
    return mapping.get(category, THEME["text_muted"])
