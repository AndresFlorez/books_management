from typing import Dict
from dateutil.parser import parse as parse_date

def proccess_filters(filters: Dict) -> Dict:
    processed_filters = {}
    for key, value in filters.items():
        value = cast_value(value)
        if "__" in key:
            field, operator = key.split("__", 1)
            if field not in processed_filters:
                processed_filters[field] = {}
            if operator in ["gte", "lte", "gt", "lt"]:
                processed_filters[field][f"${operator}"] = value
        else:
            processed_filters[key] = value
    return processed_filters

def cast_value(value: str) -> str:
    try:
        return int(value)
    except ValueError: pass

    try:
        return float(value)
    except ValueError: pass

    try:
        return parse_date(value)
    except ValueError: pass

    return value
