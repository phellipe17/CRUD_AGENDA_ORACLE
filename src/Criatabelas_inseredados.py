from conexion.oracle_queries import OracleQueries

def create_tables(query:str):
    list_of_commands = query.split(";")

    oracle = OracleQueries(can_write=True)
    oracle.connect()

    for command in list_of_commands:    
        if len(command) > 0:
            print(command)
            try:
                oracle.executeDDL(command)
                print("Successfully executed")
            except Exception as e:
                print(e)            

def generate_records(query:str, sep:str=';'):
    list_of_commands = query.split(sep)

    oracle = OracleQueries(can_write=True)
    oracle.connect()

    for command in list_of_commands:    
        if len(command) > 0:
            print(command)
            oracle.write(command)
            print("Successfully executed")

def run():

    with open("../sql/Criar_tabelas_agenda.sql") as f:
        query_create = f.read()

    print("Criando tabelas...")
    create_tables(query=query_create)
    print("Tabelas criadas com sucesso!")

    with open("../sql/Inserir_valores.sql") as f:
        query_generate_records = f.read()

    print("Inserindo valores...")
    generate_records(query=query_generate_records)
    print("Valores inseridos com sucesso!")


if __name__ == '__main__':
    run()