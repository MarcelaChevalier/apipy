def validar_idproduto(idproduto: int) -> bool:
    return (int(idproduto) > 0 and int(idproduto) <= 1000)

def validar_nome(nome: str) -> bool:
    nome = nome.strip()
    return (len(nome) > 0 and len(nome) <= 30)

def validar_preço(preço: str) -> bool:
    preço = preço.strip()
    return (len(preço) > 0 and len(preço) <= 15)

def validar_quantidade(quantidade: int) -> bool:
    return (int(quantidade) > 0 and int(quantidade) <= 1000)
    


