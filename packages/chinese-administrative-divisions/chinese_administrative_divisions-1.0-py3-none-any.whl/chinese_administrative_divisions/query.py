# query.py
from .data import administrative_divisions

def get_division_name(code):
    """根据行政区划代码获取单位名称"""
    return administrative_divisions.get(code, "未找到对应的行政区划信息")

def get_division_code(name):
    """根据单位名称获取行政区划代码"""
    for code, division_name in administrative_divisions.items():
        if division_name.strip() == name.strip():
            return code
    return "未找到对应的行政区划代码"