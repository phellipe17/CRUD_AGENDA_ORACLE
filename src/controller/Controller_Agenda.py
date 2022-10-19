from model.Agenda import Agenda
from conexion.oracle_queries import OracleQueries

class Controller_Agenda:
    def __init__(self):
        pass
        
    def inserir_agenda(self) -> Agenda:
        ''' Ref.: https://cx-oracle.readthedocs.io/en/latest/user_guide/plsql_execution.html#anonymous-pl-sql-blocks'''
        
        # Cria uma nova conexão com o banco
        oracle = OracleQueries()
        # Recupera o cursos para executar um bloco PL/SQL anônimo
        cursor = oracle.connect()
        # Cria a variável de saída com o tipo especificado
        output_value = cursor.var(int)

        #Solcita ao usuário que insira o cpf a ser vinculado na agenda
        cpf_nova_agenda = input("CPF (CPF que cadastrou ao cadastrar uma pessoa): ")

        nome_nova_agenda = oracle.sqlToDataFrame(f"select nome from pessoa where cpf = {cpf_nova_agenda}")

        endereco_nova_agenda = input('Endereco (Novo): ')
        telefone_nova_agenda = input('Telefone (Novo): ')
        email_nova_agenda = input('Email (novo): ')

        # Cria um dicionário para mapear as variáveis de entrada e saída
        data = dict(cpf_agenda=cpf_nova_agenda, nome_pessoa = nome_nova_agenda, endereco_agenda=endereco_nova_agenda, telefone_agenda=telefone_nova_agenda, email_agenda=email_nova_agenda )
        # Executa o bloco PL/SQL anônimo para inserção do novo produto e recuperação da chave primária criada pela sequence
        cursor.execute("""
        begin
            insert into Dados (cpf, nomepessoa, endereco, telefone, e_mail) values(:cpf_agenda, :nome_pessoa, :endereco_agenda, :telefone_agenda, :email_agenda );
        end;
        """, data)        
        oracle.conn.commit()
        # Recupera os dados da nova agenda criada transformando em um DataFrame
        df_agenda = oracle.sqlToDataFrame(f"select cpf, nomepessoa, endereco, telefone, e_mail from Dados where cpf = {cpf_nova_agenda}")
        # Cria um novo objeto Produto
        novo_agenda = Agenda(df_agenda.cpf_agenda.values[0], df_agenda.nome_pessoa.values[0], df_agenda.endereco_agenda.values[0], df_agenda.telefone_agenda.values[0], df_agenda.email_agenda.values[0])
        # Exibe os atributos do novo produto
        print(novo_agenda.to_string())
        # Retorna o objeto novo_produto para utilização posterior, caso necessário
        return novo_agenda

    def atualizar_agenda(self) -> Agenda:
        # Cria uma nova conexão com o banco que permite alteração
        oracle = OracleQueries(can_write=True)
        oracle.connect()

        # Solicita ao usuário o código do produto a ser alterado
        cpf_agenda = int(input("Cpf da Pessoa vinculada a agenda que irá alterar: "))        

        # Verifica se o produto existe na base de dados
        if not self.verifica_existencia_produto(oracle, cpf_agenda):
            # Solicita o novo endereco para a agenda
            novo_endereco_agenda = input("Endereco (Novo): ")
            novo_telefone_agenda = input("Telefone (Novo): ")
            novo_email_agenda = input('Email (Novo): ')
            # Atualiza a descrição do produto existente
            oracle.write(f"update Dados set endereco = '{novo_endereco_agenda}' where cpf = {cpf_agenda}")
            oracle.write(f"update Dados set telefone = '{novo_telefone_agenda}' where cpf = {cpf_agenda}")
            oracle.write(f"update Dados set email = '{novo_email_agenda}' where cpf = {cpf_agenda}")
            # Recupera os dados do novo produto criado transformando em um DataFrame
            df_agenda = oracle.sqlToDataFrame(f"select cpf, nomepessoa, endereco, telefone, email from Dados where cpf = {cpf_agenda}")
            # Cria um novo objeto Produto
            agenda_atualizado = Agenda(df_agenda.endereco_agenda.values[0], df_agenda.telefone_agenda.values[0], df_agenda.email_agenda.values[0])
            # Exibe os atributos do novo produto
            print(agenda_atualizado.to_string())
            # Retorna o objeto produto_atualizado para utilização posterior, caso necessário
            return agenda_atualizado
        else:
            print(f"O código {cpf_agenda} não existe.")
            return None

    def excluir_agenda(self):
        # Cria uma nova conexão com o banco que permite alteração
        oracle = OracleQueries(can_write=True)
        oracle.connect()

        # Solicita ao usuário o código do produto a ser alterado
        codigo_agenda = int(input("Código da agenda que irá excluir: "))        

        # Verifica se o produto existe na base de dados
        if not self.verifica_existencia_agenda(oracle, codigo_agenda):            
            # Recupera os dados do novo produto criado transformando em um DataFrame
            df_agenda = oracle.sqlToDataFrame(f"select id_agenda, cpf, nomepessoa, endereco, telefone, email from Dados where id_agenda = {codigo_agenda}")
            # Revome o produto da tabela
            oracle.write(f"delete from Dados where id_agenda = {codigo_agenda}")            
            # Cria um novo objeto Produto para informar que foi removido
            agenda_excluido = Agenda(df_agenda.endereco_agenda.values[0], df_agenda.telefone_agenda.values[0], df_agenda.email_agenda.values[0])
            # Exibe os atributos do produto excluído
            print("Produto Removido com Sucesso!")
            print(agenda_excluido.to_string())
        else:
            print(f"O código {codigo_agenda} não existe.")

    def verifica_existencia_agenda(self, oracle:OracleQueries, codigo:int=None) -> bool:
        # Recupera os dados do novo produto criado transformando em um DataFrame
        df_produto = oracle.sqlToDataFrame(f"select id_agenda, cpf, nomepessoa, endereco, telefone, email from Dados where id_agenda = {codigo}")
        return df_produto.empty