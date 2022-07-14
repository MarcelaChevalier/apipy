def validar_id(id: int) -> bool:
    return (int(id) > 0 and int(id) <= 1000)

def validar_nome(nome: str) -> bool:
    nome = nome.strip()
    return (len(nome) > 0 and len(nome) <= 30)

def validar_cpf(cpf: str) -> bool:
    cpf = cpf.strip()
    return (len(cpf) > 0 and len(cpf) <= 15)
    
def validar_email(email: str) -> bool:
    email = email.strip()
    return (len(email) > 0 and len(email) <= 100)


def validar_telefone(telefone: str) -> bool:
    telefone = telefone.strip()
    return (len(telefone) > 0 and len(telefone) <= 15)

def validar_celular(celular: str) -> bool:
    celular = celular.strip()
    return (len(celular) > 0 and len(celular) <= 15)

