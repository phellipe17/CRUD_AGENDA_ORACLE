from mailbox import NotEmptyError


select p.id_pessoa
    , p.nome
    , p.cpf
    from pessoa p
  order by p.id_pessoa