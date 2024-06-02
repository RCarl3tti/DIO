



def menu():
    menu = """
    ============MENU============
    [D]  - Depositar
    [S]  - Sacar
    [E]  - Extrato
    [NC] - Criar nova conta
    [LC] - Listar contas
    [NU] - Criar novo usuário
    [Q]  - Sair
    
    ============================ 
    => """
    return input(menu).upper()
  
def depositar(saldo, valor, extrato, /):
    if valor > 0:
        saldo += valor
        extrato += f"Depósito:\tR$ {valor:.2f}\n"
        print("\n=== Depósito realizado com sucesso! ===")
    else:
        print("\n### Operação falhou! O valor informado é inválido. ###")

    return saldo, extrato   
   
  
def sacar(*, saldo, valor, extrato, limite, numero_saques, limite_saques):
    excedeu_limite = valor > limite
    excedeu_saldo = valor > saldo
    excedeu_saques = numero_saques >= limite_saques
    
    if excedeu_limite or excedeu_saldo or excedeu_saques:
        print("\n### Operação inválida! ###")
        if excedeu_limite:
            print("Limite de saque excedido!")
        if excedeu_saldo:
            print("Saldo insuficiente!")
        if excedeu_saques:
            print("Limite de saques diários excedido!")
    else:
        saldo -= valor
        extrato += f"Saque:\tR$ {valor:.2f}\n"
        numero_saques += 1
        print("\n=== Saque realizado com sucesso! ===")
    
    return saldo, extrato, numero_saques








def extrato(saldo,/,*,extrato):
    pass
def criar_usuario(usuarios):
    pass
def filtrar_usuarios(cpf, usuarios):
    pass
def criar_conta(agencia, numero_conta, usuarios):
    pass
def listar_contas(contas):
    pass
def main():

