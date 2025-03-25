import os
import time
import shutil
import os.path
import datetime
from requests import requests

# Selenium
import selenium
from selenium import webdriver
from selenium.webdriver import Chrome
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.action_chains import ActionChains

# Adlib
from Adlib.api import *
from Adlib.utils import *
from Adlib.logins import *
from Adlib.virtaus import *
from Adlib.funcoes import * 
from Adlib.utils import meses
from Adlib.funcoes import *
from Adlib.virtaus import *
from Adlib.integracao import *
 
from Adlib.utils import meses
from Adlib.integracao import integracaoVirtaus
 
 
# Telegram Tokens
tokenImportarDoc = '1930575882:AAH0bP6m7k2XeV6fH3Q9l2Z5Q3Q'
chatIdImportarDoc = '-1001272680219'
 
from Adlib.api import EnumBanco, EnumProcesso, putStatusRobo, EnumStatus

# Telegram Tokens

tokenImportarDoc = '1930575882:AAH0bP6m7k2XeV6fH3Q9l2Z5Q3Q'
chatIdImportarDoc = '-1001272680219'



# Explicitação de itens que serão exportados ao importar `libs`
__all__ = [
    "os", 'shutil',"time",'datetime', 'sleep', 'requests',
    'dataEscolha','meses',
    "selenium", "webdriver", 'setupDriver',"Service", "Keys", "ChromeDriverManager",'Chrome',
    "Adlib", "integracaoVirtaus", "EnumBanco", 'esperarElemento', 'esperarElementos',"WebDriverWait", 'getCredenciais','clickCoordenada',
    'mensagemTelegram', 'selectOption','aguardarDownload', 'ActionChains',
    'putStatusRobo', 'EnumStatus', 'EnumProcesso',  
    'loginBMG', 'loginVirtaus', 'loginDaycoval', 'assumirSolicitacao', 'FiltrosSolicitacao','getNumeroSolicitacao',
    'tokenImportarDoc', 'chatIdImportarDoc',
    'BeautifulSoup', 'mapping', "os", 'shutil',' requests',"time",'datetime', 
    'dataEscolha','meses', 
    "selenium", "webdriver", 'setupDriver',"Service", "Keys", "ChromeDriverManager",'Chrome',
    "Adlib", "integracaoVirtaus", "EnumBanco", 'esperarElemento', 'esperarElementos',"WebDriverWait", 'getCredenciais','clickCoordenada', 
    'mensagemTelegram', 'selectOption','aguardarDownload', 'ActionChains', 
    'putStatusRobo', 'EnumStatus', 'EnumProcesso',   
    'loginBMG', 'loginVirtaus', 'loginVirtaus', 'loginDaycoval','loginVirtaus', 'assumirSolicitacao', 'FiltrosSolicitacao',
    'tokenImportarDoc', 'chatIdImportarDoc'
]
