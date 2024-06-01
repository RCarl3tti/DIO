menu = """

[D] - Depositar
[S] - Sacar
[E] - Extrato
[Q] - Sair

=>"""

saldo = 0
limite = 500
extrato = ""
numero_saques = 0
LIMITE_SAQUES = 3

while True:
    opcao = input(menu).upper()
    
    
    if opcao == "D":
        valor = float(input("Digite o valor a ser depositado: "))
        while valor <= 0:
            valor = float(input("Digite um valor válido: "))
        saldo += valor
        extrato += f"Depósito de R$ {valor:.2f}\n"
        print("=" * 40)
        print("Depósito efetuado com sucesso!")
        print("=" * 40)
    
    elif opcao == "S":
        valor = float(input("Digite o valor a ser sacado: "))
        excedeu_limite = valor > limite
        excedeu_saldo = valor > saldo
        excedeu_saques = numero_saques >= LIMITE_SAQUES
        
        if excedeu_limite or excedeu_saldo or excedeu_saques:
            print("=" * 40)
            print("Operação inválida!")
            print("=" * 40)
            if excedeu_limite:
                print("Limite de saque excedido!")
            if excedeu_saldo:
                print("Saldo insuficiente!")
            if excedeu_saques:
                print("Limite de saques diários excedido!")
        elif valor > 0:
            saldo -= valor
            extrato += f"Saque de R$ {valor:.2f}\n"
            numero_saques += 1
            print("=" * 40)
            print("Saque efetuado com sucesso!")
            print("=" * 40)
            
    elif opcao == "E":
        print("=" * 40)
        print("Extrato:")
        print("Não foram realizadas movimentações." if not extrato else extrato)
        print("=" * 40)
        print(f"Saldo: R$ {saldo:.2f}")
        print("=" * 40)
                
    elif opcao == "Q":
        print("=" * 40)
        print("Sistema encerrado!")
        print("=" * 40)
        break