"""
Rounding utilities for premium calculation.
"""
from decimal import Decimal, ROUND_HALF_UP


def round_to_three_decimals(value: float) -> float:
    """
    Round value to 3 decimal places (for intermediate calculations).
    
    Args:
        value: Value to round
    
    Returns:
        Value rounded to 3 decimal places
    """
    return float(Decimal(str(value)).quantize(Decimal('0.001'), rounding=ROUND_HALF_UP))


def round_to_integer(value: float) -> int:
    """
    Round value to nearest integer (for final premium amounts).
    
    Args:
        value: Value to round
    
    Returns:
        Value rounded to nearest integer
    """
    return int(Decimal(str(value)).quantize(Decimal('1'), rounding=ROUND_HALF_UP))


def apply_rounding_step(value: float, step_name: str = "") -> float:
    """
    Apply intermediate rounding (3 decimal places) with optional logging.
    
    Args:
        value: Value to round
        step_name: Optional name for logging the step
    
    Returns:
        Rounded value
    """
    rounded_value = round_to_three_decimals(value)
    
    if step_name:
        print(f"  {step_name}: {value:.6f} → {rounded_value:.3f}")
    
    return rounded_value
