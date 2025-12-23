def format_currency(amount: float) -> str:
    return f"${amount:,.2f}"

def mask_card_number(card_num: str) -> str:
    return "*" * 12 + card_num[-4:]
