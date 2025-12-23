from datetime import datetime
import re

def parse_date(date_str: str) -> datetime:
    """YYYY-MM-DD 形式または YY/MM/DD 形式をパースする"""
    if re.match(r"\d{4}-\d{2}-\d{2}", date_str):
        return datetime.strptime(date_str, "%Y-%m-%d")
    elif re.match(r"\d{2}/\d{2}/\d{2}", date_str):
        return datetime.strptime(date_str, "%y/%m/%d")
    raise ValueError(f"Invalid date format: {date_str}")

def format_date_display(dt: datetime) -> str:
    """画面表示用に MM/DD/YY 形式に変換する"""
    return dt.strftime("%m/%d/%y")

def get_current_timestamp() -> datetime:
    return datetime.utcnow()
