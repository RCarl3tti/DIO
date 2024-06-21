from abc import ABC, abstractmethod
from datetime import datetime

class ContaIterador:
    def __init__(self, contas):
        self.contas = contas
        self._index = 0
    
    def __iter__(self):
        return self
    
    def __next__(self):
        try:
            conta = self.contas[self._index]
            return f"""\
            Agência:\t{conta.agencia}
            C/C:\t\t{conta.numero}
            Titular:\t{conta.cliente.nome}
            Saldo:\t\tR$ {conta.saldo:.2f}
            """
        except IndexError:
            raise StopIteration()
        finally:
            self._index += 1    

class Cliente:
    def __init__(self, endereco):
        self.endereco = endereco
        self.contas = []
        self.indice_conta = 0
        
    def realizar_transacao(self, conta, transacao):
        if len(conta.historico.transacoes_do_dia()) >= 10:
            print('@@@ Limite de transações diárias excedido @@@')
            return
        transacao.registrar(conta)
        
    def adicionar_conta(self, conta):
        self.contas.append(conta)
        
class PessoaFisica(Cliente):
    def __init__(self, nome, data_nascimento, cpf, endereco):
        super().__init__(endereco)
        self.nome = nome
        self.data_nascimento = data_nascimento
        self.cpf = cpf

class Conta:
    def __init__(self, numero, cliente):
        self._saldo = 0
        self._numero = numero
        self._agencia = '0001'
        self._cliente = cliente
        self._historico = Historico()
    
    @classmethod
    def nova_conta(cls, cliente, numero):
        return cls(numero, cliente)
    
    @property
    def saldo(self):
        return self._saldo
    
    @property
    def numero(self):
        return self._numero
    
    @property
    def agencia(self):
        return self._agencia
    
    @property
    def cliente(self):
        return self._cliente
    
    @property
    def historico(self):
        return self._historico
    
    def sacar(self, valor):
        saldo = self.saldo
        excedeu_saldo = valor > saldo
        
        if excedeu_saldo:
            print('@@@ Saldo insuficiente @@@')
        
        elif valor > 0:
            self._saldo -= valor
            print("\n=== Saque realizado com sucesso! ===")
            return True
        else:
            print('@@@ Operação falhou, valor informado é inválido @@@')
        
        return False
    
    def depositar(self, valor):
        if valor > 0:
            self._saldo += valor
            print("\n=== Depósito realizado com sucesso! ===")
            
        else:
            print('@@@ Operação falhou, valor informado é inválido @@@')
            return False
        
        return True
    
class ContaCorrente(Conta):
    def __init__(self, numero, cliente, limite=500, limite_saques=3):
        super().__init__(numero, cliente)
        self._limite = limite
        self._limite_saques = limite_saques
        
    def sacar(self, valor):
        numero_saques = len(
            [transacao for transacao in self.historico.transacoes if transacao['tipo'] == Saque.__name__]
        )

        excedeu_limite = valor > self.limite
        excedeu_limite_saques = numero_saques >= self.limite_saques
    
        if excedeu_limite:
            print('@@@ Valor excede o limite de saque @@@')
    
        elif excedeu_limite_saques:
            print('@@@ Limite de saques excedido @@@')
    
        else:
            return super().sacar(valor)
        
        return False
    
    def __str__(self):
        return f"""\
            Agência:\t{self.agencia}
            C/C:\t\t{self.numero}
            Titular:\t{self.cliente.nome}
            """

class Historico:
    def __init__(self):
        self._transacoes = []
        
    @property
    def transacoes(self):
        return self._transacoes
    
    def adicionar_transacao(self, transacao):
        self._transacoes.append(
            {
                "tipo": transacao.__class__.__name__,
                "valor": transacao.valor,
                "data": datetime.now().strftime
                ('%d/%m/%Y %H:%M:%S'),
            }
        )
    
    def gerar_relatorio(self, tipo_transacao=None):
        for transacao in self._transacoes:
            if not tipo_transacao is None or transacao['tipo'].lower == tipo_transacao.lower():
                yield transacao
                
    def transacoes_do_dia(self):
        data_atual = datetime.now().strftime('%d/%m/%Y')
        transacoes = []
        for transacao in self.transacoes:
            data_transacao = datetime.strptime(transacao['data'], '%d/%m/%Y %H:%M:%S').date()
            if data_atual == data_transacao:
                transacoes.append(transacao)
        return transacoes
        
class Transacao(ABC):
    @property
    @abstractmethod
    def valor(self):
        pass
    
    @abstractmethod
    def registrar(self, conta):
        pass
    
class Saque(Transacao):
    def __init__(self, valor):
        self._valor = valor
        
    @property
    def valor(self):
        return self._valor
    
    def registrar(self, conta):
        sucesso_transacao = conta.sacar(self.valor)
        
        if sucesso_transacao:
            conta.historico.adicionar_transacao(self)
            
class Deposito(Transacao):
    def __init__(self, valor):
        self._valor = valor
        
    @property
    def valor(self):
        return self._valor
    
    def registrar(self, conta):
        sucesso_transacao = conta.depositar(self.valor)
        
        if sucesso_transacao:
            conta.historico.adicionar_transacao(self)
        
def log_transacao(func):
    def envelope(*args, **kwargs):
        resultado = func(*args, **kwargs)
        print(f"{datetime.now()}: {func.__name__.upper()}")   
        return resultado
    return envelope

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

def filtrar_cliente(cpf, clientes):
    clientes_filtrados = [cliente for cliente in clientes if cliente.cpf == cpf]
    return clientes_filtrados[0] if clientes_filtrados else None

def recuperar_conta_cliente(cliente):
    if not cliente.contas:
        print('@@@ Cliente não possui contas cadastradas @@@')
        return 
    return cliente.contas[0]


@log_transacao
def depositar(clientes):
    cpf = input('Informe o CPF: ')
    cliente = filtrar_cliente(cpf, clientes)
    
    if not cliente:
        print('@@@ Cliente não encontrado! @@@')
        return

    valor = float(input('Informe o valor do depósito: '))
    transacao = Deposito(valor)
    
    conta = recuperar_conta_cliente(cliente)
    if not conta:
        return
    
    cliente.realizar_transacao(conta, transacao)


@log_transacao
def sacar(clientes):
    cpf = input('Informe o CPF do cliente: ')
    cliente = filtrar_cliente(cpf, clientes)
    
    if not cliente:
        print('@@@ Cliente não encontrado! @@@')
        return
    
    valor = float(input('Informe o valor do saque: '))
    transacao = Saque(valor)
    
    conta = recuperar_conta_cliente(cliente)
    if not conta:
        return
    
    cliente.realizar_transacao(conta, transacao)


@log_transacao
def exibir_extrato(clientes):
    cpf = input('Informe o CPF do cliente: ')
    cliente = filtrar_cliente(cpf, clientes)
    
    if not cliente:
        print('@@@ Cliente não encontrado! @@@')
        return
    
    conta = recuperar_conta_cliente(cliente)
    if not conta:
        return
    
    print("\n=================== Extrato ===================")
    extrato = ""
    tem_transacao = False
    for transacao in conta.historico.gerar_relatorio():
        tem_transacao = True
        extrato += f"{transacao['tipo']}:\n\tR$ {transacao['valor']:.2f}"
        
    if not tem_transacao:
        extrato = "Sem transações realizadas"
    
    print(extrato)
    print(f"\nSaldo atual: R$ {conta.saldo:.2f}")    
    print("===============================================")
    
    

@log_transacao
def criar_conta(numero_conta, clientes, contas):
    cpf = input('Informe o CPF do cliente: ')
    cliente = filtrar_cliente(cpf, clientes)
    
    if not cliente:
        print('@@@ Cliente não encontrado! @@@')
        return
    
    conta = ContaCorrente.nova_conta(cliente=cliente, numero=numero_conta)
    contas.append(conta)
    cliente.contas.append(conta)
    
    print('=== Conta criada com sucesso! ===')

def listar_contas(contas):
    for conta in ContaIterador(contas):
        print("=" * 40)
        print(conta)

@log_transacao
def criar_cliente(clientes):
    cpf = input('Informe o CPF: ')
    cliente = filtrar_cliente(cpf, clientes)
    
    if cliente:
        print('@@@ Cliente já cadastrado! @@@')
        return
    
    nome = input('Informe o nome completo: ')
    data_nascimento = input('Informe a data de nascimento: ')
    endereco = input('Informe o endereço (logradouro, nro - bairro - cidade/sigla do estado): ')
    
    cliente = PessoaFisica(nome=nome, data_nascimento=data_nascimento, cpf=cpf, endereco=endereco)
    clientes.append(cliente)
    
    print('=== Cliente criado com sucesso! ===')

def main():
    clientes = []
    contas = []
    
    while True:
        opcao = menu()
        
        if opcao == 'D':
            depositar(clientes)
        
        elif opcao == 'S':
            sacar(clientes)
            
        elif opcao == 'E':
            exibir_extrato(clientes)
        
        elif opcao == 'NU':
            criar_cliente(clientes)
        
        elif opcao == 'NC':
            numero_conta = len(contas) + 1
            criar_conta(numero_conta, clientes, contas)
            
        elif opcao == 'LC':
            listar_contas(contas)
        
        elif opcao == 'Q':
            print('Saindo...')
            print('Sistema encerrado!')
            break
        
if __name__ == '__main__':
    main()