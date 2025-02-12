def validate_balance(balance, item_price):
    if balance < item_price:
        return False
    return True
