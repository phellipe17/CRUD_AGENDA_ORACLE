from controller.Controller_Agenda import Controller_Agenda
from controller.controller_pessoa import Controller_Pessoa
import reports
from utils import config

tela_inicial = "SPLASH SCREEN DO PARAGUAI"

def inserir(opcao_inserir:int=0):
    if opcao_inserir==1:
        Controller_Pessoa.inserir_pessoa()
    elif opcao_inserir==2:
        Controller_Agenda.inserir_agenda()
        

def atualizar(opcao_atualizar:int=0):
    if opcao_atualizar==1:
        Controller_Pessoa.atualizar_pessoa()
    elif opcao_atualizar==2:
        Controller_Agenda.atualizar_agenda()

def excluir(opcao_excluir:int=0):
    if opcao_excluir==1:
       Controller_Pessoa.excluir_pessoa()
    elif opcao_excluir==2:
        Controller_Agenda.excluir_agenda()

def run():
    print(tela_inicial)
    #splashscreen aqui
    config.clear_console(1)

    while True:
        print(config.MENU_PRINCIPAL)
        opcao= int(input("Escolha uma opção [entre 1 a 5]: "))
        config.clear_console(1)

        if opcao==1:#Listar
            print(config.MENU_RELATORIOS)
            opcao_relatorio=int(input("Escolha uma opção de 0 a 3: "))
            config.clear_console(1)

            reports(opcao_relatorio)

            config.clear_console(1)
        
        elif opcao==2: #Inserir
            print(config.MENU_ENTIDADES)
            opcao_inserir=int(input("Escolha uma opção 1 ou 2: "))
            config.clear_console(1)

            inserir(opcao_inserir)

            config.clear_console(1)
        
        elif opcao ==3:#atualizar
            print(config.MENU_ENTIDADES)
            opcao_atualizar=int(input("Escolha opção 1 ou 2: "))
            config.clear_console(1)

            atualizar(opcao_atualizar)

            config.clear_console(1)

        elif opcao==4:#excluir
            decisao="n"
            decisao=input("Deseja realmente excluir alguma entidade? ")
            if (decisao =="s" or "sim" or "Sim" or "SIM"):    
                print(config.MENU_ENTIDADES)
                opcao_excluir=int(input("Escolha opção 1 ou 2: "))
                config.clear_console(1)

                excluir(opcao_excluir)

                config.clear_console(1)
            else:
                print("Retornando")
        
        elif opcao==5:#saindo:
            print(tela_inicial.get_updated_screen())
            config.clear_console()
            print("Obrigado por utilizar o nosso sistema.")
            exit(0)

        else:
            print("Opção incorreta.")
            exit(1)



if __name__=='__main__':
    run()