class Pessoa:
    def __init__(self, 
                 nome:str=None,
                 CPF:str=None 
                ):
        self.set_nome(nome)
        self.set_CPF(CPF)
        

    def set_CPF(self, CPF:str):
        self.CPF = CPF

    def set_nome(self, nome:str):
        self.nome = nome

    def get_CPF(self) -> str:
        return self.CPF

    def get_nome(self) -> str:
        return self.nome

    def to_string(self) -> str:
        return f"CPF: {self.get_CPF()} | Nome: {self.get_nome()}"