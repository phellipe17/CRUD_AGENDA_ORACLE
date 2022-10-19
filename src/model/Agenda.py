class Agenda:

    def __init__(self,nomepessoa:str, id_pessoa:int, endereco:str,telefone:str, e_mail:str ):
        self.setNomepessoa(nomepessoa)
        self.setId_pessoa(id_pessoa)
        self.set_endereco(endereco)
        self.set_telefone(telefone)
        self.setE_mail(e_mail)

    def set_endereco(self, endereco:str):
        self.endereco=endereco
    

    def set_telefone(self, telefone:str):
        self.telefone=telefone

    def setId_pessoa(self, id_pessoa:int):
        self.id_pessoa=id_pessoa
    
    def setE_mail(self, e_mail:str):
        self.e_mail=e_mail
    
    def setNomePEssoa(self,nomepessoa):
        self.nomepessoa=nomepessoa

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


