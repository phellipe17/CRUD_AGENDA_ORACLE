from controller.controller_pessoa import Controller_Cliente
import reports
from utils import config

tela_inicial = "Olá"

def inserir(opcao_inserir:int=0):
    if opcao_inserir==1:
        Controller_Cliente().inserir_pessoa()
    elif opcao_inserir==2:
        print("colocar método")
        #método de inserir registro para agenda

def atualizar(opcao_atualizar:int=0):
    if opcao_atualizar==1:
        Controller_Cliente.atualizar_pessoa()

def excluir(opcao_excluir:int=0):
    if opcao_excluir==1:
       Controller_Cliente.excluir_pessoa()

def run():
    print(tela_inicial)
    #splashscreen aqui
    config.clear_console(1)

    while True:
        print(config.MENU_PRINCIPAL)
        opcao= int(input("Escolha uma opção [entre 1 a 5]: "))
        config.clear_console(1)

        if opcao==1:
            print(config.MENU_RELATORIOS)
            opcao_relatorio=int(input("Escolha uma opção de 0 a 3: "))
            config.clear_console(1)

            reports(opcao_relatorio)

            config.clear_console(1)



if __name__=='__main__':
    run()