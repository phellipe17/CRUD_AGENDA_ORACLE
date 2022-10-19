from pydoc import cli
from model.Agenda import Agenda
from model.Pessoa import Pessoa
from controller.controller_pessoa import Controller_Pessoa
from conexion.oracle_queries import OracleQueries

class Controller_Agenda:
    def __init__(self):
        self.ctrl_pessoa = Controller_Pessoa()
        
    def inserir_agenda(self) -> Agenda:
        ''' Ref.: https://cx-oracle.readthedocs.io/en/latest/user_guide/plsql_execution.html#anonymous-pl-sql-blocks'''
        
        # Cria uma nova conexão com o banco
        oracle = OracleQueries()
        
        # Lista as pessoas existentes para inserir na agenda
        self.listar_pessoa(oracle, need_connect=True)
        cpf = str(input("Digite o número da CPF do Pessoa: "))
        pessoa = self.valida_pessoa(oracle, cpf)
        if pessoa == None:
            return None       
            
        
        # Recupera o cursos para executar um bloco PL/SQL anônimo
        cursor = oracle.connect()
        # Cria a variável de saída com o tipo especificado
        output_value = cursor.var(int)

        # Cria um dicionário para mapear as variáveis de entrada e saída
        data = dict(codigo=output_value, cpf=pessoa.get_CPF(), nome = pessoa.get_nome)
        # Executa o bloco PL/SQL anônimo para inserção do novo produto e recuperação da chave primária criada pela sequence
        cursor.execute("""
        begin
            insert into agenda values(:cpf, :nome);
        end;
        """, data)
        # Recupera o código da nova agenda
        codigo_agenda = output_value.getvalue()
        # Persiste (confirma) as alterações
        oracle.conn.commit()
        # Recupera os dados do novo produto criado transformando em um DataFrame
        df_agenda = oracle.sqlToDataFrame(f"select id_agenda, cpf, nomepessoa, endereco, telefone, email from agenda where cpf = {cpf}")
        # Cria um novo objeto Produto
        novo_agenda = Agenda(df_agenda.codigo_agenda.values[0], pessoa)
        # Exibe os atributos da nova agenda criada
        print(novo_agenda.to_string())
        # Retorna o objeto novo_pedido para utilização posterior, caso necessário
        return novo_agenda

    def atualizar_agenda(self) -> Agenda:
        # Cria uma nova conexão com o banco que permite alteração
        oracle = OracleQueries(can_write=True)
        oracle.connect()

        # Solicita ao usuário o código da agenda a ser alterado
        codigo_agenda = int(input("Código da Agenda que irá alterar: "))        

        # Verifica se o produto existe na base de dados
        if not self.verifica_existencia_agenda(oracle, codigo_agenda):

            # Lista as pessoas para inserir na agenda
            self.listar_agendas(oracle)
            cpf = str(input("Digite o número do CPF da Pessoa: "))
            pessoa = self.valida_pessoa(oracle, cpf)
            if pessoa == None:
                return None
            

            # Atualiza a descrição da agenda existente
            oracle.write(f"update agenda set cpf = '{pessoa.get_CPF()}' where codigo_pedido = {codigo_agenda}")
            # Recupera os dados da nova agenda criado transformando em um DataFrame
            df_agenda = oracle.sqlToDataFrame(f"select id_agenda, cpf, NomePessoa, Telefone, email from agenda where id_agenda = {codigo_agenda}")
            # Cria um novo objet Agenda
            agenda_atualizado = Agenda(df_agenda.codigo_agenda.values[0], pessoa)
            # Exibe os atributos da nova agenda
            print(agenda_atualizado.to_string())
            # Retorna o objeto pedido_atualizado para utilização posterior, caso necessário
            return agenda_atualizado
        else:
            print(f"O código {codigo_agenda} não existe.")
            return None

    def excluir_agenda(self):
        # Cria uma nova conexão com o banco que permite alteração
        oracle = OracleQueries(can_write=True)
        oracle.connect()

        # Solicita ao usuário o código do produto a ser alterado
        codigo_agenda = int(input("Código do Pedido que irá excluir: "))        

        # Verifica se o produto existe na base de dados
        if not self.verifica_existencia_agenda(oracle, codigo_agenda):            
            # Recupera os dados da nova agenda criado transformando em um DataFrame
            df_agenda = oracle.sqlToDataFrame(f"select id_agenda, cpf, nomepessoa, Telefone, email from agenda where id_agenda = {codigo_agenda}")
            pessoa = self.valida_pessoa(oracle, df_agenda.cpf.values[0])
            
            opcao_excluir = input(f"Tem certeza que deseja excluir a agenda {codigo_agenda} [S ou N]: ")
            if opcao_excluir.lower() == "s":
                opcao_excluir = input(f"Tem certeza que deseja a agenda {codigo_agenda} [S ou N]: ")
                if opcao_excluir.lower() == "s":                    
                    oracle.write(f"delete from agenda where id_agenda = {codigo_agenda}")
                    # Cria um novo objeto Produto para informar que foi removido
                    agenda_excluido = Agenda(df_agenda.codigo_agenda.values[0], pessoa)
                    # Exibe os atributos do produto excluído
                    print("Agenda Removida com Sucesso!")
                    print(agenda_excluido.to_string())
        else:
            print(f"O código {codigo_agenda} não existe.")

    def verifica_existencia_agenda(self, oracle:OracleQueries, codigo:int=None) -> bool:
        # Recupera os dados da nova agenda criado transformando em um DataFrame
        df_pedido = oracle.sqlToDataFrame(f"select id_agenda, cpf, nomepessoa, Telefone, email from agenda where id_agenda = {codigo}")
        return df_pedido.empty

    def listar_pessoa(self, oracle:OracleQueries, need_connect:bool=False):
        query = """
                select c.cpf
                    , c.nome 
                from pessoa c
                order by c.nome
                """
        if need_connect:
            oracle.connect()
        print(oracle.sqlToDataFrame(query))    

    def valida_pessoa(self, oracle:OracleQueries, cpf:str=None) -> Pessoa:
        if self.ctrl_pessoa.verifica_existencia_pessoa(oracle, cpf):
            print(f"O CPF {cpf} informado não existe na base.")
            return None
        else:
            oracle.connect()
            # Recupera os dados da nova pessoa criada transformando em um DataFrame
            df_pessoa = oracle.sqlToDataFrame(f"select cpf, nome from pessoa where cpf = {cpf}")
            # Cria um novo objeto cliente
            pessoa = Pessoa(df_pessoa.cpf.values[0], df_pessoa.nome.values[0])
            return pessoa
    