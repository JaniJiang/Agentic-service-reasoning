from datetime import datetime, timedelta


def get_last_week():
    """获取上周日期"""
    today = datetime.now()
    last_week_start = today - timedelta(days=today.weekday() + 7)
    last_week_end = last_week_start + timedelta(days=6)
    last_week_start_str = last_week_start.strftime("%Y%m%d")
    last_week_end_str = last_week_end.strftime("%Y%m%d")
    week_str = f"{last_week_start_str}-{last_week_end_str}"
    return last_week_start, week_str
