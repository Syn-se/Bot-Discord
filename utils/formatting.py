def format_silver(value: float) -> str:
    """Formate un montant en silver avec séparateurs de milliers."""
    return f"{int(round(value)):,} silver".replace(",", " ")
