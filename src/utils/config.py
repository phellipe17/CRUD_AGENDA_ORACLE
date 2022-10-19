MENU_RELATORIOS="""Relatórios
1 - Pessoas cadastradas
2 - Dados de pessoas cadastrados
3 - Dados de pessoas vinculado a uma única pessoa
0 - Sair
"""

MENU_ENTIDADES = """Entidades
1 - Pessoas
2 - Dados
"""

MENU_PRINCIPAL = """Menu Principal
1 - Relatórios
2 - Inserir registro
3 - Atualizar registro
4 - Remover registro
5 - Sair
"""

# Consulta de contagem de registros por tabela
QUERY_COUNT = 'select count(1) as total_{tabela} from {tabela}'

def clear_console(wait_time:int=3):
    '''
       Esse método limpa a tela após alguns segundos
       wait_time: argumento de entrada que indica o tempo de espera
    '''
    import os
    from time import sleep
    sleep(wait_time)
    os.system("clear")