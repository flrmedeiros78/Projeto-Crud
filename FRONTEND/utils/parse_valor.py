import math

def parse_valor(v: str) -> float:
    """'1.500,00' → 1500.00"""
    result = float(v.replace(".", "").replace(",", "."))
    if not math.isfinite(result):
        raise ValueError(f"Valor inválido: '{v}'")
    # Proteção: impede salvar valores absurdos
    if result > 1_000_000_000:
        raise ValueError(f"Valor muito alto: {result:,.2f}")
    return result