--Delecoes
DROP TABLE Pessoa;
DROP TABLE Agenda;

-- Formando estrutura para tabela labdatabase.Pessoa
  CREATE TABLE pessoa (
  id_pessoa int GENERATED ALWAYS AS IDENTITY NOT NULL,
  nome varchar2(100) NOT NULL,
  cpf varchar2(17) NOT NULL,
  PRIMARY KEY (id_pessoa)
);

-- Formando estrutura para tabela basedados_agenda.Agenda
  CREATE TABLE dados (
  id_agenda int GENERATED ALWAYS AS IDENTITY NOT NULL,
  nomepessoa varchar2(100) NOT NULL,
  endereco varchar2(100) NOT NULL,
  telefone varchar2(20) DEFAULT NULL,
  e_mail varchar2(100) DEFAULT NULL,
  PRIMARY KEY (id_agenda),  
  CONSTRAINT agenda_ibfk FOREIGN KEY (id_agenda) REFERENCES pessoa (id_pessoa) ON DELETE CASCADE
);

--Join
 select * from agenda a inner join  pessoa p on a.id_agenda = p.id_pessoa;

commit;