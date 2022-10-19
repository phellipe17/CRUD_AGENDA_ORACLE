from conexion.oracle_queries import OracleQueries

class Relatorio:
    def __init__(self):
        #abre o arquivo de pessoa
        with open("sql/relatorio_dados.sql") as f:
            self.query_relatorio_pessoa=f.read()
        
        with open("sql/relatorio_dados.sql") as f:
            self.query_relatorio_dados= f.read()
    
    def get_relatorio_pessoas(self):
        # Cria uma nova conexão com o banco que permite alteração
        oracle = OracleQueries()
        oracle.connect()
        # Recupera os dados transformando em um DataFrame
        print(oracle.sqlToDataFrame(self.query_relatorio_pessoas))
        input("Pressione Enter para Sair do Relatório de Pedidos")
    
    def get_relatorio_dados(self):
        # Cria uma nova conexão com o banco que permite alteração
        oracle = OracleQueries()
        oracle.connect()
        # Recupera os dados transformando em um DataFrame
        print(oracle.sqlToDataFrame(self.query_relatorio_dados))
        input("Pressione Enter para Sair do Relatório de dados")