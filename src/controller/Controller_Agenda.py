from pydoc import cli
from model.Agenda import Agenda
from model.Pessoa import Pessoa
from controller.Controller_Pessoa import Controller_Pessoa
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
        data = dict(codigo=output_value, cpf=pessoa.get_CPF())
        # Executa o bloco PL/SQL anônimo para inserção do novo produto e recuperação da chave primária criada pela sequence
        cursor.execute("""
        begin
            insert into agenda values(:cpf, :);
        end;
        """, data)
        # Recupera o código da nova agenda
        codigo_agenda = output_value.getvalue()
        # Persiste (confirma) as alterações
        oracle.conn.commit()
        # Recupera os dados do novo produto criado transformando em um DataFrame
        df_pedido = oracle.sqlToDataFrame(f"select id_agenda, cpf, nomepessoa, endereco, telefone, email from agenda where cpf = {cpf}")
        # Cria um novo objeto Produto
        novo_pedido = Pedido(df_pedido.codigo_pedido.values[0], df_pedido.data_pedido.values[0], cliente, fornecedor)
        # Exibe os atributos do novo produto
        print(novo_pedido.to_string())
        # Retorna o objeto novo_pedido para utilização posterior, caso necessário
        return novo_pedido

    def atualizar_pedido(self) -> Pedido:
        # Cria uma nova conexão com o banco que permite alteração
        oracle = OracleQueries(can_write=True)
        oracle.connect()

        # Solicita ao usuário o código do produto a ser alterado
        codigo_pedido = int(input("Código do Pedido que irá alterar: "))        

        # Verifica se o produto existe na base de dados
        if not self.verifica_existencia_pedido(oracle, codigo_pedido):

            # Lista os clientes existentes para inserir no pedido
            self.listar_clientes(oracle)
            cpf = str(input("Digite o número do CPF do Cliente: "))
            cliente = self.valida_cliente(oracle, cpf)
            if cliente == None:
                return None

            # Lista os fornecedores existentes para inserir no pedido
            self.listar_fornecedores(oracle)
            cnpj = str(input("Digite o número do CNPJ do Fornecedor: "))
            fornecedor = self.valida_fornecedor(oracle, cnpj)
            if fornecedor == None:
                return None

            data_hoje = date.today()

            # Atualiza a descrição do produto existente
            oracle.write(f"update pedidos set cpf = '{cliente.get_CPF()}', cnpj = '{fornecedor.get_CNPJ()}', data_pedido = to_date('{data_hoje}','yyyy-mm-dd') where codigo_pedido = {codigo_pedido}")
            # Recupera os dados do novo produto criado transformando em um DataFrame
            df_pedido = oracle.sqlToDataFrame(f"select codigo_pedido, data_pedido from pedidos where codigo_pedido = {codigo_pedido}")
            # Cria um novo objeto Produto
            pedido_atualizado = Pedido(df_pedido.codigo_pedido.values[0], df_pedido.data_pedido.values[0], cliente, fornecedor)
            # Exibe os atributos do novo produto
            print(pedido_atualizado.to_string())
            # Retorna o objeto pedido_atualizado para utilização posterior, caso necessário
            return pedido_atualizado
        else:
            print(f"O código {codigo_pedido} não existe.")
            return None

    def excluir_pedido(self):
        # Cria uma nova conexão com o banco que permite alteração
        oracle = OracleQueries(can_write=True)
        oracle.connect()

        # Solicita ao usuário o código do produto a ser alterado
        codigo_pedido = int(input("Código do Pedido que irá excluir: "))        

        # Verifica se o produto existe na base de dados
        if not self.verifica_existencia_pedido(oracle, codigo_pedido):            
            # Recupera os dados do novo produto criado transformando em um DataFrame
            df_pedido = oracle.sqlToDataFrame(f"select codigo_pedido, data_pedido, cpf, cnpj from pedidos where codigo_pedido = {codigo_pedido}")
            cliente = self.valida_cliente(oracle, df_pedido.cpf.values[0])
            fornecedor = self.valida_fornecedor(oracle, df_pedido.cnpj.values[0])
            
            opcao_excluir = input(f"Tem certeza que deseja excluir o pedido {codigo_pedido} [S ou N]: ")
            if opcao_excluir.lower() == "s":
                print("Atenção, caso o pedido possua itens, também serão excluídos!")
                opcao_excluir = input(f"Tem certeza que deseja excluir o pedido {codigo_pedido} [S ou N]: ")
                if opcao_excluir.lower() == "s":
                    # Revome o produto da tabela
                    oracle.write(f"delete from itens_pedido where codigo_pedido = {codigo_pedido}")
                    print("Itens do pedido removidos com sucesso!")
                    oracle.write(f"delete from pedidos where codigo_pedido = {codigo_pedido}")
                    # Cria um novo objeto Produto para informar que foi removido
                    pedido_excluido = Pedido(df_pedido.codigo_pedido.values[0], df_pedido.data_pedido.values[0], cliente, fornecedor)
                    # Exibe os atributos do produto excluído
                    print("Pedido Removido com Sucesso!")
                    print(pedido_excluido.to_string())
        else:
            print(f"O código {codigo_pedido} não existe.")

    def verifica_existencia_pedido(self, oracle:OracleQueries, codigo:int=None) -> bool:
        # Recupera os dados do novo pedido criado transformando em um DataFrame
        df_pedido = oracle.sqlToDataFrame(f"select codigo_pedido, data_pedido from pedidos where codigo_pedido = {codigo}")
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
            cliente = Pessoa(df_pessoa.cpf.values[0], df_pessoa.nome.values[0])
            return pessoa
    