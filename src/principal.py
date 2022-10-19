from controller.controller_pessoa import Controller_Cliente
from utils import config

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
    print("Olá")



if __name__=='__main__':
    run()