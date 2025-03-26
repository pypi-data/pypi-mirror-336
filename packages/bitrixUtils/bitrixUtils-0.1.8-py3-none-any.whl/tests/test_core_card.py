import sys
import os
import json

# Adiciona o diretório do bitrix.py ao sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../bitrixUtils')))
import core
BITRIX_WEBHOOK_URL = "https://setup.bitrix24.com.br/rest/629/c0q6gqm7og1bs91k/"

fields = {
    "NAME" : "Nome Teste",
    "PHONE": [{
            "VALUE_TYPE" : "OTHER",
            "VALUE" : "+5599000000000",
            "TYPE_ID" : "PHONE"
        }],
    "EMAIL" : [{
        "VALUE_TYPE" : "OTHER",
        "VALUE" : "teste.jc@gmail.com",
        "TYPE_ID" : "EMAIL"
    }],
    "UF_CRM_1739896985967" : "0000000000000", #CNPJ
    "UF_CRM_1742922446857" : "JESUS" #SOCIOS

}
contact = core.createContact_new(BITRIX_WEBHOOK_URL,fields,LOG=False)

print(json.dumps(contact, indent=4, ensure_ascii=False))
