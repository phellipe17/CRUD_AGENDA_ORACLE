from model.Pessoa import Pessoa
from conexion.oracle_queries import OracleQueries

class Controller_Pessoa:
    def __init__(self):
        pass
        
    def inserir_pessoa(self) -> Pessoa:
        ''' Ref.: https://cx-oracle.readthedocs.io/en/latest/user_guide/plsql_execution.html#anonymous-pl-sql-blocks'''
        
        # Cria uma nova conexão com o banco que permite alteração
        oracle = OracleQueries(can_write=True)
        oracle.connect()

        # Solicita ao usuario o novo CPF
        cpf = input("CPF (Novo): ")

        if self.verifica_existencia_cliente(oracle, cpf):
            # Solicita ao usuario o novo nome
            nome = input("Nome (Novo): ")
            # Insere e persiste uma nova pessoa
            oracle.write(f"insert into pessoa values ('{cpf}', '{nome}')")
            # Recupera os dados do novo cliente criado transformando em um DataFrame
            df_pessoa = oracle.sqlToDataFrame(f"select cpf, nome from pessoa where cpf = '{cpf}'")
            # Cria um novo objeto Pessoa
            novo_pessoa = Pessoa(df_pessoa.cpf.values[0], df_pessoa.nome.values[0])
            # Exibe os atributos do novo cliente
            print(novo_pessoa.to_string())
            # Retorna o objeto novo_pessoa para utilização posterior, caso necessário
            return novo_pessoa
        else:
            print(f"O CPF {cpf} já está cadastrado.")
            return None

    def atualizar_pessoa(self) -> Pessoa:
        # Cria uma nova conexão com o banco que permite alteração
        oracle = OracleQueries(can_write=True)
        oracle.connect()

        # Solicita ao usuário o código do cliente a ser alterado
        cpf = int(input("CPF da pessoa que deseja alterar o nome: "))

        # Verifica se a pessoa existe na base de dados
        if not self.verifica_existencia_cliente(oracle, cpf):
            # Solicita a nova descrição de pessoa
            novo_nome = input("Nome (Novo): ")
            # Atualiza o nome do cliente existente
            oracle.write(f"update pessoa set nome = '{novo_nome}' where cpf = {cpf}")
            # Recupera os dados do novo cliente criado transformando em um DataFrame
            df_pessoa = oracle.sqlToDataFrame(f"select cpf, nome from pessoa where cpf = {cpf}")
            # Cria um novo objeto cliente
            pessoa_atualizado = Pessoa(df_pessoa.cpf.values[0], df_pessoa.nome.values[0])
            # Exibe os atributos da nova pessoa
            print(pessoa_atualizado.to_string())
            # Retorna o objeto pessoa_atualizado para utilização posterior, caso necessário
            return pessoa_atualizado
        else:
            print(f"O CPF {cpf} não existe.")
            return None

    def excluir_pessoa(self):
        # Cria uma nova conexão com o banco que permite alteração
        oracle = OracleQueries(can_write=True)
        oracle.connect()

        # Solicita ao usuário o CPF da pessoa a ser alterada
        cpf = int(input("CPF da Pessoa que irá excluir: "))        

        # Verifica se a Pessoa existe na base de dados
        if not self.verifica_existencia_pessoa(oracle, cpf):            
            # Recupera os dados da nova pessoa criado transformando em um DataFrame
            df_pessoa = oracle.sqlToDataFrame(f"select cpf, nome from pessoa where cpf = {cpf}")
            # Revome a pessoa da tabela
            oracle.write(f"delete from pessoa where cpf = {cpf}")            
            # Cria um novo objeto Pessoa para informar que foi removido
            pessoa_excluido = Pessoa(df_pessoa.cpf.values[0], df_pessoa.nome.values[0])
            # Exibe os atributos do cliente excluído
            print("Pessoa Removida com Sucesso!")
            print(pessoa_excluido.to_string())
        else:
            print(f"O CPF {cpf} não existe.")

    def verifica_existencia_pessoa(self, oracle:OracleQueries, cpf:str=None) -> bool:
        # Recupera os dados da nova Pessoa criado transformando em um DataFrame
        df_pessoa = oracle.sqlToDataFrame(f"select cpf, nome from pessoa where cpf = {cpf}")
        return df_pessoa.empty