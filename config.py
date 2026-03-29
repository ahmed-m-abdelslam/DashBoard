import os
from dotenv import load_dotenv

load_dotenv()

# API
GROQ_API_KEY = os.getenv("GROQ_API")
GROQ_MODEL = "llama-3.3-70b-versatile"
AI_TEMPERATURE = 0.3
AI_TIMEOUT = 15

# App
APP_PORT = 8050
APP_HOST = "127.0.0.1"
APP_DEBUG = False
MAX_FILE_SIZE_MB = 10
MAX_FILE_SIZE_BYTES = MAX_FILE_SIZE_MB * 1024 * 1024
SUPPORTED_EXTENSIONS = {"xlsx", "xlsm", "xls", "csv"}

# Theme
THEME = {
    "bg": "#f8fafc",
    "card_bg": "#ffffff",
    "dark": "#0f172a",
    "dark2": "#1e293b",
    "dark3": "#334155",
    "text": "#1e293b",
    "text_light": "#64748b",
    "text_muted": "#94a3b8",
    "border": "#e2e8f0",
    "border_light": "#f1f5f9",
    "success": "#10b981",
    "success_light": "#d1fae5",
    "warning": "#f59e0b",
    "warning_light": "#fef3c7",
    "danger": "#ef4444",
    "danger_light": "#fee2e2",
    "info": "#3b82f6",
    "info_light": "#dbeafe",
    "purple": "#8b5cf6",
    "purple_light": "#ede9fe",
    "indigo": "#6366f1",
    "cyan": "#06b6d4",
    "pink": "#ec4899",
    "teal": "#14b8a6",
    "orange": "#f97316",
}

PROJECT_COLORS = [
    {"main": "#6366f1", "light": "#eef2ff", "gradient": "linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%)"},
    {"main": "#0ea5e9", "light": "#f0f9ff", "gradient": "linear-gradient(135deg, #0ea5e9 0%, #06b6d4 100%)"},
    {"main": "#f97316", "light": "#fff7ed", "gradient": "linear-gradient(135deg, #f97316 0%, #fb923c 100%)"},
    {"main": "#ec4899", "light": "#fdf2f8", "gradient": "linear-gradient(135deg, #ec4899 0%, #f472b6 100%)"},
    {"main": "#14b8a6", "light": "#f0fdfa", "gradient": "linear-gradient(135deg, #14b8a6 0%, #2dd4bf 100%)"},
    {"main": "#8b5cf6", "light": "#f5f3ff", "gradient": "linear-gradient(135deg, #8b5cf6 0%, #a78bfa 100%)"},
    {"main": "#ef4444", "light": "#fef2f2", "gradient": "linear-gradient(135deg, #ef4444 0%, #f87171 100%)"},
]

FONT = {
    "xs": "11px", "sm": "12.5px", "md": "14px", "lg": "17px",
    "xl": "20px", "xxl": "26px", "xxxl": "34px",
}

COLUMN_PATTERNS = {
    "project_name": ["project name", "project"],
    "current_stage": ["current stage", "stage"],
    "opening_date": ["opening date", "open date"],
    "proposed_budget": ["proposed budget"],
    "client_budget": ["client budget"],
    "orders_placed": ["orders placed"],
    "orders_in_progress": ["orders in progress"],
    "currency": ["currency"],
    "proc_started": ["proc process started", "procurement started"],
    "total_packages": ["total no package", "total packages"],
    "packages_completed": ["ordering completed"],
    "packages_in_progress": ["ordering in progress"],
    "delivery_started": ["delivery process started"],
    "total_pos": ["total no po raised", "total po"],
    "delivered_pos": ["total delivered"],
    "concerns": ["concern"],
    "overall_proc": ["overall procurement", "overall proc"],
}

CONCERN_KEYWORDS = {
    "Supplier": ["supplier", "vendor", "manufacturer"],
    "Timeline": ["delay", "late", "behind", "slow"],
    "Cost": ["cost", "price", "budget", "expensive", "overrun"],
    "Quality": ["quality", "defect", "damage", "reject"],
    "Approval": ["approval", "pending", "waiting", "hold"],
    "Logistics": ["lead time", "shipping", "logistics", "freight"],
}
