import pythonzimbra.communication
from pythonzimbra.communication import Communication
import pythonzimbra.tools
from pythonzimbra.tools import auth
import urllib


class GetZimbra():
    def __init__(self, hostname, user, password, signature):
        self.url = f'https://{hostname}:7071/service/admin/soap'
        self.usr = user 
        self.__password = password
        self.signature = signature


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


    def modify_signature(self,func, ma):
        """
        <ModifyAccountRequest id="{value-of-zimbra-id}"> ## ModifyAccountRequest
        (<a n="{key}" /> ## Attr)*
        </ModifyAccountRequest>
        """
        if 'Error get_account: ' in func:
            return func

        else:
            accountid = func['id']

        self.request.add_request(
            'ModifyAccountRequest',
            {
                "id": accountid, 'a': ma                
            },
            'urn:zimbraAdmin'
        )
        response = self.comm.send_request(self.request)

        if not response.is_fault():
            #import ipdb; ipdb.set_trace()
            return [a['_content'] for a in response.get_response(2)['ModifyAccountResponse']['account'][0]['a'] if a['n'] == 'zimbraSignatureName']

        else:
            return f'Error get_account: {response.get_fault_message()}'

    def get_account(self,account):
        """
        <GetAccountRequest [applyCos="{apply-cos} (0|1)"] [attrs="{request-attrs}"]> ## GetAccountRequest
        <account by="{acct-selector-by} (adminName|appAdminName|id|foreignPrincipal|name|krb5Principal)">{key}</account> ## AccountSelector
        </GetAccountRequest>
        """
        self.request.add_request(
            "GetAccountRequest",
            {   
                'attrs': 'zimbraSignatureId',
                "account": {
                    "_content": account,
                    "by": "name"
                }
            },
            "urn:zimbraAdmin"
        )
        response = self.comm.send_request(self.request)

        if not response.is_fault():
            #import ipdb; ipdb.set_trace()
            return response.get_response(1)['GetAccountResponse']['account'][0]

        else:
            return f'Error get_account: {response.get_fault_message()}'


