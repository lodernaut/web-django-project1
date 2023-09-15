def is_positive_number(value):
    try:
        value = float(value)
    except ValueError:
        return False
    return value > 0
