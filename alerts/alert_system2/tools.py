"""Simple tools."""

def string_to_bool(a):
    """Return boolean from string."""
    if type(a) == type(True):
        return a
    if a.lower().strip() == "true":
        return True
    if a.isdigit():
        a = int(float(a))
        if a != 0:
            return True
    return False
