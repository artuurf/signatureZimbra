# signatureZimbra

Script Python para incluir assinatura no Zimbra pela api soap.
Inclua a assinatura em HTML na variável signaturez, e execute o arquivo .py com os parametros abaixo:

python3 arquivo.py -a admin -p passaword -c arquivo.csv -H url -s

arquivo deverá estar da seguinte forma: 
email, nome, sobrenome, cargo, telefone
teste@gmail.com, vitão, meu casal, talarico, 4002-8922
teste2@gmail.com, Winderson, Nunes, chifrudo, 5090-1234

OBS: Por algum motivo o Zimbra não consegue consultar o ID da assinatura logo depois que aplica. 
Recomendado aplicar a assinatura em todas as contas, em seguida após 5 minutos aplicar com default para novo emails.

Para aplicar o default para enviar novos emails, resposta e encaminhamentos com a assinatura, basta colocar -s True
