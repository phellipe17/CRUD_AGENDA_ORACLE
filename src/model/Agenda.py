class Agenda:

    def __init__(self,id_agenda:int,cpf:str,nomepessoa:str, id_pessoa:int, endereco:str,telefone:str, e_mail:str ):
        self.setId_agenda(id_agenda)
        self.setCpf(cpf)
        self.setNomepessoa(nomepessoa)
        self.setId_pessoa(id_pessoa)
        self.set_endereco(endereco)
        self.set_telefone(telefone)
        self.setE_mail(e_mail)

    def setId_agenda(self,id_agenda:int):
        self.id_agenda=id_agenda

    def setCpf(self,cpf:str):
        self.cpf=cpf

    def set_endereco(self, endereco:str):
        self.endereco=endereco
    
    def set_telefone(self, telefone:str):
        self.telefone=telefone

    def setId_pessoa(self, id_pessoa:int):
        self.id_pessoa=id_pessoa
    
    def setE_mail(self, e_mail:str):
        self.e_mail=e_mail
    
    def setNomepessoa(self,nomepessoa):
        self.nomepessoa=nomepessoa

    def getId_agenda(self)->int:
        return self.id_agenda
    
    def getCpf(self)->str:
        return self.cpf

    def get_Endereco(self)->str:
        return self.endereco
     
    def getTelefone(self)->str:
        return self.telefone

    def getE_mail(self)->str:
        return self.e_mail 
    
    def getId_pessoa(self)->int:
        return self.id_pessoa
    def getNomePessoa(self)->str:
        return self.nomepessoa
    
    def toString(self)->str:
        return f"Nome: {self.getNomePessoa} |Telefone: {self.getTelefone} | E-mail: {self.getE_mail} | Endereco: {self.get_Endereco}"


