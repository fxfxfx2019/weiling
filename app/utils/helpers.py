"""
通用辅助函数
"""
from datetime import datetime
from typing import Dict, Any

def format_datetime(dt: datetime) -> str:
    """格式化日期时间"""
    return dt.strftime("%Y-%m-%d %H:%M:%S")

def filter_dict(data: Dict[str, Any], valid_keys: list) -> Dict[str, Any]:
    """过滤字典，只保留指定的键"""
    return {k: v for k, v in data.items() if k in valid_keys}

def remove_none_values(data: Dict[str, Any]) -> Dict[str, Any]:
    """移除字典中的 None 值"""
    return {k: v for k, v in data.items() if v is not None}

def validate_password(password: str) -> bool:
    """验证密码强度"""
    if len(password) < 8:
        return False
    # 至少包含一个数字
    if not any(c.isdigit() for c in password):
        return False
    # 至少包含一个字母
    if not any(c.isalpha() for c in password):
        return False
    return True 