from typing import Literal, Optional, SupportsIndex


def limit_range(
    value: float,
    operator: Literal["+", "-", "*", "/"],
    ratio: float,
    min_value: float = 0.01,
    max_value: float = 1,
    n_digits: Optional[SupportsIndex] = 2,
) -> float | int:
    """
    Limit the value to a specified range and round it to a specified number of decimal places.

    Args:
        value (float): The value to limit.
        operator (str): The operator to use for limiting the value. Can be "+", "-", "*", or "/".
        ratio (float): The ratio to apply to the value.
        min_value (float): The minimum value of the range.
        max_value (float): The maximum value of the range.
        n_digits (int): The number of decimal places to round to.

    Returns:
        float: The limited and rounded value.
    """
    match operator:
        case "+":
            return round(max(min(value + ratio, max_value), min_value), n_digits)
        case "-":
            return round(max(min(value - ratio, max_value), min_value), n_digits)
        case "*":
            return round(max(min(value * ratio, max_value), min_value), n_digits)
        case "/":
            if ratio == 0:
                return round(max(min(value, max_value), min_value), n_digits)
            else:
                return round(max(min(value / ratio, max_value), min_value), n_digits)
