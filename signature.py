import pythonzimbra.communication
from pythonzimbra.communication import Communication
import pythonzimbra.tools
from pythonzimbra.tools import auth
import urllib
import argparse
from argparse import RawTextHelpFormatter
import csv

"""
Script Python para incluir assinatura no Zimbra pela api soap.

Inclua a assinatura em HTML na variável self.signature, e execute o arquivo .py com os parametros abaixo:

python3 arquivo.py -a admin -p passaword -c arquivo.csv -H url

arquivo deverá estar da seguinte forma: 

email, nome, sobrenome, cargo, telefone
teste@gmail.com, vitão, meu casal, talarico, 4002-8922
teste2@gmail.com, Winderson, Nunes, chifrudo, 5090-1234

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
                    \n\tExample: \n--archive /home/arquivo.csv', required=True)
parser.add_argument('-H', '--host', action='store', dest='hostname',
                    help='webmail URL', required=True)
"""
parser.add_argument('-n', '--name', action='store', dest='name',
                    help='name in signature', required=True)
"""
argslist = parser.parse_args()



class GetZimbra():
    def __init__(self, hostname, user, password, signature):
        self.url = f'https://{hostname}:7071/service/admin/soap'
        self.usr = user 
        self.__password = password
        self.signature = signature
        self.attr = 'zimbraPrefMailSignatureHTML'



    def connect(self):
        #import ipdb; ipdb.set_trace()
        try:
            self.comm = Communication(self.url)
            self.__token = auth.authenticate(self.url, self.usr, self.__password, admin_auth=True)
            self.request = self.comm.gen_request(token=self.__token, set_batch=True)

            return 'Conectado'

        except urllib.error.URLError as E:
        # catastrophic error. bail.
            return f'Erro na conexão: {E}'

    
    def get_accountinf(self,account):
        """
        <GetAccountInfoRequest> ## GetAccountInfoRequest
        <account by="{acct-selector-by} (adminName|appAdminName|id|foreignPrincipal|name|krb5Principal)">{key}</account> ## AccountSelector
        </GetAccountInfoRequest>
        """
        self.request.add_request(
            'GetAccountInfoRequest',
        {

                "account": {
                    "_content": account,
                    "by": "name"
                }
            },
            'urn:zimbraAdmin'
        )
        response = self.comm.send_request(self.request)

        if not response.is_fault():
            return response.get_response(1)['GetAccountInfoResponse']['a'][0]['_content']


        else:
            return f'Error get_account: {response.get_fault_message()}'
    

    def modify_signature(self,func, signature):
        """
        <ModifyAccountRequest id="{value-of-zimbra-id}"> ## ModifyAccountRequest
        (<a n="{key}" /> ## Attr)*
        </ModifyAccountRequest>
        """
        if 'Error get_account: ' in func:
            return func

        else: 
            accountid = func

        self.request.add_request(
            'ModifyAccountRequest',
            {
                "id": accountid, 'a': [
                    {'n': self.attr, '_content': signature}
                ]                
            },
            'urn:zimbraAdmin'
        )
        response = self.comm.send_request(self.request)

        if not response.is_fault():
            #import ipdb; ipdb.set_trace()
            return [a['_content'] for a in response.get_response(2)['ModifyAccountResponse']['account'][0]['a'] if a['n'] == self.attr]

        else:
            return f'Error get_account: {response.get_fault_message()}'


if __name__ == '__main__':
    zmteste = GetZimbra(argslist.hostname, argslist.admin, argslist.password)
    print(zmteste.connect())

    with open(argslist.archive, 'r') as file:
        csvreader = csv.reader(file)
        header = next(csvreader)
        for row in csvreader:
            """
            email, nome, sobrenome, cargo, telefone
            row[0] = email
            row[1] = nome
            row[2] = sobrenome
            row[3] = cargo
            row[4] = telefone
            """
            print(f'Aplicando assinatura em {row[0]} ...')
            
            signaturez = f'<div><table style="color: #000000; font-size: 13.3333px; font-style: normal; font-weight: 400; letter-spacing: normal; text-transform: none; white-space: normal; word-spacing: 0px; font-family: "verdana" , "helvetica" , sans-serif; background-color: #fdfdfd; width: 435px; table-layout: fixed; height: 109px;" cellpadding="3px" border="0px"><tbody><tr><td style="font-family: "verdana" , "arial" , "helvetica" , sans-serif; font-size: 14px; width: 150px;"><span style="color: #000080;"><strong>{row[1]}</strong></span></td><td rowspan="3" style="font-family: "verdana" , "arial" , "helvetica" , sans-serif; font-size: 14px; width: 1px;"><img alt="" src="http://suporte.email.com.br/assinatura/sig_inova_pipe1.png" style="width: 4px; height: 75px;" /></td><td style="font-family: "verdana" , "arial" , "helvetica" , sans-serif; font-size: 14px; width: 284px;"><strong><span style="font-size: 11px; color: #000080;">&nbsp;<span class="Object" id="OBJ_PREFIX_DWT11535_com_zimbra_phone" style="color: #006990;">55 11 5090-1234</span></span></strong></td></tr><tr><td rowspan="2" style="font-family: "verdana" , "arial" , "helvetica" , sans-serif; font-size: 14px; width: 150px;"><img alt="" src="https://webmail.inova.com.br/home/felipe.maeda@inova.net/Briefcase/A/inova_sig.png" style="color: #262262; font-weight: bold; text-align: center; background-color: #ffffff; width: 150px; height: 35px;" /></td><td style="font-family: "verdana" , "arial" , "helvetica" , sans-serif; font-size: 14px; width: 284px;"><span style="color: #000080; font-size: 10pt; font-family: "verdana" , "helvetica" , sans-serif;"><b>&nbsp;Rua Gomes de Carvalho, 1629 - 1&nbsp; &nbsp;Andar - Vila&nbsp;</b></span><span style="color: #000080; font-family: "verdana" , "helvetica" , sans-serif;"><span style="font-size: 13.3333px;"><b>Ol&iacute;mpia</b></span></span><span style="color: #000080; font-size: 10pt; font-family: "verdana" , "helvetica" , sans-serif;"><b>&nbsp;</b></span><br /><span style="color: #000080;"><span style="font-size: 11px;"><b>&nbsp;04547-006&nbsp;</b></span></span><span style="color: #000080; font-size: 11px;"><b>S&atilde;o Paulo | SP Brasil&nbsp;</b></span></td></tr><tr><td style="font-family: "verdana" , "arial" , "helvetica" , sans-serif; font-size: 14px; width: 284px;"><span style="color: #000080;">&nbsp;</span><span style="color: #000080;"><span class="Object" id="OBJ_PREFIX_DWT11536_com_zimbra_url" style="color: #006990;"><span class="Object" id="OBJ_PREFIX_DWT1780_com_zimbra_url" style="color: #005a95;"><a href="http://www.inova.com.br/" rel="nofollow noopener noreferrer nofollow noopener noreferrer nofollow noopener noreferrer nofollow noopener noreferrer nofollow noopener noreferrer nofollow noopener noreferrer nofollow noopener noreferrer nofollow noopener noreferrer nofollow noopener noreferrer nofollow noopener noreferrer nofollow noopener noreferrer nofollow noopener noreferrer nofollow noopener noreferrer nofollow noopener noreferrer nofollow noopener noreferrer nofollow noopener noreferrer" style="color: #006990;" target="_blank">www.inova.com.br</a></span></span></span></td></tr><tr></tr></tbody></table><br style="color: #000000; font-style: normal; font-weight: 400; letter-spacing: normal; text-indent: 0px; text-transform: none; white-space: normal; word-spacing: 0px; font-family: "verdana" , "helvetica" , sans-serif; font-size: 13.3333px; background-color: #fdfdfd;" /><div style="color: #000000; font-style: normal; font-weight: 400; letter-spacing: normal; text-indent: 0px; text-transform: none; white-space: normal; word-spacing: 0px; font-family: "verdana" , "helvetica" , sans-serif; font-size: 13.3333px; background-color: #fdfdfd;"><span style="color: #0000ff;">Agora a Inova &eacute; Penso!&nbsp;<span class="Object" id="OBJ_PREFIX_DWT11537_com_zimbra_url" style="color: #006990;"><span class="Object" id="OBJ_PREFIX_DWT1781_com_zimbra_url" style="color: #005a95;"><a href="https://www.penso.com.br/penso-compra-inova-tecnologias" rel="noopener nofollow noopener noreferrer nofollow noopener noreferrer nofollow noopener noreferrer nofollow noopener noreferrer nofollow noopener noreferrer nofollow noopener noreferrer nofollow noopener noreferrer nofollow noopener noreferrer nofollow noopener noreferrer nofollow noopener noreferrer" style="color: #006990;" target="_blank"><strong>Clique aqui</strong></a></span></span>&nbsp;e saiba mais!</span></div></div>'

            print(zmteste.modify_signature(zmteste.get_accountinf(row[0]), signaturez))
