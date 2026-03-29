import io
import base64
import pandas as pd
from config import MAX_FILE_SIZE_BYTES, SUPPORTED_EXTENSIONS
from data.extractor import extract_projects_from_sheet
from data.metrics import compute_all_metrics
from data.validators import validate_project


class ParseError(Exception):
    pass


def validate_upload(contents, filename):
    if not filename:
        raise ParseError("No filename provided.")
    ext = filename.lower().rsplit(".", 1)[-1] if "." in filename else ""
    if ext not in SUPPORTED_EXTENSIONS:
        raise ParseError(f"Unsupported file type: .{ext}")
    content_string = contents.split(",")[1]
    decoded = base64.b64decode(content_string)
    if len(decoded) > MAX_FILE_SIZE_BYTES:
        raise ParseError(f"File too large ({len(decoded)/1024/1024:.1f}MB). Max: {MAX_FILE_SIZE_BYTES/1024/1024:.0f}MB")
    return ext, decoded


def parse_file(contents, filename):
    ext, decoded = validate_upload(contents, filename)
    buf = io.BytesIO(decoded)

    raw_projects = []
    if ext == "csv":
        df = pd.read_csv(buf)
        raw_projects.extend(extract_projects_from_sheet(df))
    else:
        engine = "openpyxl" if ext in ("xlsx", "xlsm") else "xlrd"
        xls = pd.ExcelFile(buf, engine=engine)
        for sheet_name in xls.sheet_names:
            df = pd.read_excel(xls, sheet_name=sheet_name)
            if not df.dropna(how="all").empty:
                raw_projects.extend(extract_projects_from_sheet(df))

    if not raw_projects:
        raise ParseError("No valid project data found in file.")

    processed = []
    for project in raw_projects:
        project = compute_all_metrics(project)
        project = validate_project(project)
        processed.append(project)

    return processed
