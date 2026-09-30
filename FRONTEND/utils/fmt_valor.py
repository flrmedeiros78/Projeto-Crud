#--------------------------------------------------- 
# FUNÇÃO AUXILIAR: FORMATAR VALOR MONETÁRIO
#--------------------------------------------------- 
def fmt_valor(v):
    """Converte um número para formato brasileiro: 1500.50 -> 'R$ 1.500,50'"""
    num = float(v)
    # Proteção: se o valor é irrealmente grande, não tenta formatar
    if num > 1_000_000_000:  # acima de 1 bilhão, algo está errado
        return "Valor corrompido"
    s = f"{num:,.2f}"
    s = s.replace(",", "x").replace(".", ",").replace("x", ".")
    return f"R$ {s}"