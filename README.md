# signatureZimbra

Script Python para incluir assinatura no Zimbra pela api soap utilizando arquivo csv.

Inclua a assinatura em HTML na variável self.signature, e execute o arquivo .py com os parametros abaixo: 

python3 arquivo.py -a admin -p passaword -c arquivo.csv -H url

arquivo deverá estar da seguinte forma: 

email, nome, sobrenome, cargo, telefone
teste@gmail.com, vitão, meu casal, talarico, 4002-8922
teste2@gmail.com, Winderson, Nunes, chifrudo, 5090-1234
