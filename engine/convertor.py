import numpy as np


def to_float(value):
    if not value:
        return np.nan
    elif isinstance(value, str):
        value = value.strip()
        try:
            value = float(value)
        except ValueError:
            pass
    return value
