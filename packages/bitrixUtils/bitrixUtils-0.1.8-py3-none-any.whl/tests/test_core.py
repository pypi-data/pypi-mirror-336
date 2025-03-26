import sys
import os
import json

# Adiciona o diretório do bitrix.py ao sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../bitrixUtils')))
import core
BITRIX_WEBHOOK_URL = "https://setup.bitrix24.com.br/rest/629/c0q6gqm7og1bs91k/"

# select_fields = [
#     "UF_CRM_1701275490640", #CNPJ
#     "UF_CRM_1708446996746", #CONTRACT_MODEL_ID
#     "UF_CRM_1727441490980", #CONSULTOR_SITTAX
#     "UF_CRM_1727438279465", #CONSULTOR_ACESSORIAS
#     "UF_CRM_1727441546022", #VALOR_LICENCA_SITTAX
#     "UF_CRM_1727438009508", #VALOR_LICENCA_ACESSORIAS
#     "UF_CRM_1727441557582", #VALOR_MENSALIDADE_SITTAX
#     "UF_CRM_1727437983987", #VALOR_MENSALIDADE_ACESSORIAS
#     "UF_CRM_1739387711215", #PACOTE_SITTAX
#     "UF_CRM_1739476124760", #PACOTE_ACESSORIAS
#     "UF_CRM_1723638730243", #REVENDA
#     "UF_CRM_1725555192239" #QUADRO_SOCIETARIO
#     ]

# comp = core.searchCompanyByField(BITRIX_WEBHOOK_URL, "UF_CRM_1701275490640", "15.123.560/0001-00",select_fields, LOG=False)
# fields = {
#     "TITLE" : "Empresa Jesus Teste",
#     "EMAIL" : [{"VALUE": "contato@empresa.com", "VALUE_TYPE": "OTHER"}],
#     "PHONE" : [{"VALUE": "11999999999", "VALUE_TYPE": "OTHER"}],
#     "UF_CRM_1701275490640" : "00.000.000/0001-00",
#     "UF_CRM_1708446996746" : 655,
#     "UF_CRM_1727441490980" : "Teste Consultor",
#     "UF_CRM_1727438279465" : "Teste Consultor",
#     "UF_CRM_1727441546022" : 1000,
#     "UF_CRM_1727438009508" : 1000,
#     "UF_CRM_1727441557582" : 2000,
#     "UF_CRM_1727437983987" : 2000,
#     "UF_CRM_1739387711215" : 20,
#     "UF_CRM_1739476124760" : 20,
#     "UF_CRM_1723638730243" : 691,
#     "UF_CRM_1725555192239" : "Nome Teste"
# }
spa = [158,187]
comp = core.getDealsByCompany(BITRIX_WEBHOOK_URL,14479,spa,LOG=True)
print(json.dumps(comp, indent=4, ensure_ascii=False))