

def validar_idhistorico(idhistorico: int) -> bool:
    return (int(idhistorico) > 0 and int(idhistorico) <= 10000000000)


def validar_idproduto(idproduto: int) -> bool:
    return (int(idproduto) > 0 and int(idproduto) <= 10000000000)

def validar_idcliente(idcliente: int) -> bool:
    return (int(idcliente) > 0 and int(idcliente) <= 100000000)
