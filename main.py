from signature import GetZimbra
import argparse
from argparse import RawTextHelpFormatter
import csv

"""
Script Python para incluir assinatura no Zimbra pela api soap.

Inclua a assinatura em HTML na variável signaturez, e execute o arquivo .py com os parametros abaixo:

python3 arquivo.py -a admin -p passaword -c arquivo.csv -H url -s

arquivo deverá estar da seguinte forma: 

email, nome, sobrenome, cargo, telefone
teste@gmail.com, vitão, meu casal, talarico, 4002-8922
teste2@gmail.com, Winderson, Nunes, chifrudo, 5090-1234


OBS: Por algum motivo o Zimbra não consegue consultar o ID da assinatura logo depois que aplica. 
Recomendado aplicar a assinatura em todas as contas, em seguida após 5 minutos aplicar com os atributos para novo emails, resposta/encaminhamentos colocar a assinatura. 

Para aplicar a assinatura como default para enviar novos emails, resposta e encaminhamentos, basta colocar -s True
"""

parser = argparse.ArgumentParser(
    description='Authenticates as zimbra administrator and returns a list\
    \nof accounts and their attrs(previously defined on zimbraAtributes.',
    formatter_class=RawTextHelpFormatter)
parser.add_argument('-a', '--admin', action='store', dest='admin',
                    help='Zimbra Admin Account to authenticate on server',
                    required=True)
parser.add_argument('-p', '--pass', action='store', dest='password',
                    help='Zimbra Admin Password String', required=True)
parser.add_argument('-c', '--archive', action='store', dest='archive',
                    help='archive to get accounts info\
                    \n\tExample: \n--archive arquivo.csv', required=True)
parser.add_argument('-H', '--host', action='store', dest='hostname',
                    help='webmail URL', required=True)

parser.add_argument('-s', '--setdefault', action='store', dest='setdefault',
                    help='set default the signature', nargs='?', const=False, type=bool, required=True)


argslist = parser.parse_args()

zmteste = GetZimbra(argslist.hostname, argslist.admin, argslist.password, signature=None)

f = open(argslist.archive, 'r', encoding='utf-8-sig')

with f:
    reader = csv.reader(f)
    for row in reader:
        #import ipdb; ipdb.set_trace()
        """
        email, nome, sobrenome, cargo, telefone
        row[0] = email
        row[1] = nome
        row[2] = sobrenome
        row[3] = cargo
        row[4] = telefone
        """
        zmteste.connect()
        if not argslist.setdefault:
            print(f'Aplicando assinatura em {row[0]} ...')
            
            signaturez = f'<table width="0" height="0" border="0" cellpadding="0" cellspacing="0" id="tabela" style="padding-right:10px; text-align: top; border-bottom: 5px solid #264ca1; border-collapse: collapse; ">	  <tbody><tr style="border-collapse: collapse;">      <td width="auto" height="10" rowspan="3" style="padding-right:10px; border-right: 2px solid #778899;">        <span id="logo_ass" style="padding-bottom:2px"><img src="https://servicos.sepaco.org.br/sepacoapp/assinatura/imagens/Logo_Hospital.png" width="180" height="132" style="padding:0 2px"></span><br><br>          </td>    <td width="200" height="100" rowspan="4" style="font-family: helvetica,arial,sans-serif; font-size: 9px; padding-left: 10px" td="">        <span id="logo_ass" style="padding-bottom:2px"> </span><br><br><span align="center" style="font-family: helvetica,arial,sans-serif; font-size: 9px;">            </span><b><a id="nome_usuario" style="color:#000000; font-size:11px; text-align: top;">Vitão</a></b><br><a id="depto_usuario" style="color:#000000; font-size:11px;">Meu Casal</a><br><br><strong id="titulo_ass" style="font-size:11px;"></strong><table width="200px" height="50px" border="0" cellpadding="0" cellspacing="0" style="padding-right:10px; border-collapse: collapse;">                    <tbody><tr>              <td style="border-top: 2px solid #778899;"><img src="https://servicos.sepaco.org.br/sepacoapp/assinatura/imagens/telefone.png" alt="fone" width="20" height="20"></td>              <td style="border-top: 2px solid #778899;"><a id="telefone_usuario" style="font-size:11px; ">(69) 4002-8922</a></td>            </tr>            <tr>              <td><img src="https://servicos.sepaco.org.br/sepacoapp/assinatura/imagens/email.png" alt="fone" width="20" height="20"></td>              <td><span id="site_ass" style="font-size:11px; "><a "www.sepaco.org.br"="" style="text-decoration:" none;"="">www.sepaco.org.br</a></span></td>            </tr>            <tr>              <td><img src="https://servicos.sepaco.org.br/sepacoapp/assinatura/imagens/site.png" alt="fone" width="20" height="20"></td>              <td><a id="email_usuario" style="font-size:11px; ">teste@gmail.com</a></td>            </tr>            <tr>              <td><img src="https://servicos.sepaco.org.br/sepacoapp/assinatura/imagens/endereco.png" alt="fone" width="20" height="20"></td>              <td><a style="font-size:11px; ">Rua Vergueiro, 4210 - Vila Mariana</a></td>            </tr>        </tbody></table>    </td>    <td height="70" style="text-align: le" td=""><span style="width: 11.2795%; text-align: center; height: 40px; border-collapse: collapse;"><img src="https://servicos.sepaco.org.br/sepacoapp/assinatura/imagens/enfe2.png" alt="fone" width="80" height="30"></span></td>  </tr>  <tr style="height: 48px; border-collapse: collapse;">    <td style="text-align: right; width: 20px; height: 48px;"><span style="width: 11.2795%; text-align: center; height: 70px; border-collapse: collapse;"></span></td>    </tr>  <tr style="border-collapse: collapse; width: 600px; ">    <td style="text-align: center; width: 20px;" td=""><br><a href="https://pt-br.facebook.com/hospitalsepaco/"><img src="https://servicos.sepaco.org.br/sepacoapp/assinatura/imagens/facebook.png" alt="Facebook" width="18" height="16" data-filename="facebook.png"></a><img src="https://s3.amazonaws.com/htmlsig-assets/spacer.gif" width="2"><a href="https://www.linkedin.com/company/hospital-sepaco"><img src="https://servicos.sepaco.org.br/sepacoapp/assinatura/imagens/linkedin.png" alt="LinkedIn" width="18" height="16" data-filename="linkedin.png"></a><img src="https://s3.amazonaws.com/htmlsig-assets/spacer.gif" width="2"><a href="https://www.instagram.com/hospitalsepaco/"><img src="https://servicos.sepaco.org.br/sepacoapp/assinatura/imagens/instagram.png" alt="Instagram" width="18" height="16" data-filename="instagram.png"></a><img src="https://s3.amazonaws.com/htmlsig-assets/spacer.gif" width="2">  </td></tr></tbody></table>'
            
            ma = [
                {'n': 'zimbraPrefMailSignatureEnabled', '_content': 'TRUE'},
                {'n': 'zimbraSignatureName', '_content': 'New signature'},
                {'n': 'zimbraPrefMailSignatureHTML', '_content': signaturez},
            ]
            
            print(zmteste.modify_signature(zmteste.get_account(row[0]), ma))
        
        else:
            zmteste.connect()
            signatureid = zmteste.get_account(row[0])['a'][0]['_content']

            mas = [
                {'n': 'zimbraPrefDefaultSignatureId', '_content': signatureid},
                {'n': 'zimbraPrefForwardReplySignatureId', '_content': signatureid}
            ]
            print(zmteste.modify_signature(zmteste.get_account(row[0]), mas))
            
    print('Contas finalizadas.')

