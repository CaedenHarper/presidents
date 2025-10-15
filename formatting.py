__all__ = ["format_as_percent"]

def format_as_percent(n: int, d: int) -> str:
    """Format a numerator and denominator as a percent to two decimal places."""
    return f"{(n / d * 100) if d > 0 else 0:.2f}%"
