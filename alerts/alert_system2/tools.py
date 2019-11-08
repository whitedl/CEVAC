"""Simple tools."""


def string_to_bool(a):
    """Return boolean from string."""
    if isinstance(a, bool):
        return a
    if a.lower().strip() == "true":
        return True
    if a.isdigit():
        a = int(float(a))
        if a != 0:
            return True
    return False


def verbose_print(verbose_bool, message):
    """Print a message if verbose_bool."""
    if verbose_bool:
        print(message)
