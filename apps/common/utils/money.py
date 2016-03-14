import math

def convert_to_cents(amount):
    """
    converts dollars to cents

    Args:
        amount (Decimal): Amount in dollars

    Returns:
        (int): Amount in cents
    """
    cents, dollars = math.modf(amount)
    return (int(dollars) * 100) + int(cents * 100)
