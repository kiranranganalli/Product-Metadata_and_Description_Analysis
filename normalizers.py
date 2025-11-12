import re

def to_grams(value: float, unit: str | None):
    if value is None or unit is None:
        return None
    u = unit.lower().strip()
    if u in ["g", "gram", "grams"]:
        return float(value)
    if u in ["kg", "kilogram", "kilograms"]:
        return float(value) * 1000.0
    if u in ["oz", "ounce", "ounces"]:
        return float(value) * 28.3495
    if u in ["lb", "lbs", "pound", "pounds"]:
        return float(value) * 453.592
    return None

def to_milliliters(value: float, unit: str | None):
    if value is None or unit is None:
        return None
    u = unit.lower().strip()
    if u in ["ml", "milliliter", "milliliters"]:
        return float(value)
    if u in ["l", "liter", "liters"]:
        return float(value) * 1000.0
    if u in ["fl_oz", "floz", "fluid_ounce", "fluid_ounces"]:
        return float(value) * 29.5735
    return None

def norm_key(brand: str | None, name: str | None):
    def clean(s: str):
        s = s.lower()
        s = re.sub(r"[^a-z0-9]+", "-", s)
        return re.sub(r"-+", "-", s).strip("-")
    b = clean(brand) if brand else "na"
    n = clean(name) if name else "na"
    return f"{b}:{n}"
