import os
from pprint import pprint
import re
import sys
import time
import msal
import shutil
import inspect
import requests
import datetime
import subprocess
from pathlib import Path
from Adlib.api import *
from Adlib.utils import meses
from urllib.parse import parse_qs, urlparse
from selenium import webdriver
from selenium.webdriver import Chrome
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.ui import Select, WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.actions.action_builder import ActionBuilder


TOKEN_CAPTCHA = "7505814396:AAHQvtr0ltePOLKp88awG7WHB6lksKkNaR0"
CHAT_ID_CAPTCHA = "-4095757991"


from functools import wraps

class TabDriver:
    """
    A proxy class that represents a single tab in a multi-tab Chrome instance.
    Every method call will first ensure the tab's window handle is active.
    """
    def __init__(self, driver: webdriver.Chrome, index: int):
        self.driver = driver
        self.index = index
        self.handle = driver.window_handles[index]

    def __getattribute__(self, name):
        # Retrieve attribute using the base object method
        attr = object.__getattribute__(self, name)
        
        # We don't want to wrap special or internal methods
        if callable(attr) and not name.startswith("__"):
            @wraps(attr)
            def wrapped(*args, **kwargs):
                driver = object.__getattribute__(self, "driver")
                handle = object.__getattribute__(self, "handle")
                if driver.current_window_handle != handle:
                    driver.switch_to.window(handle)
                return attr(*args, **kwargs)
            return wrapped
        
        return attr

    def __getattr__(self, name):
        """
        Delegate attribute lookup to the underlying driver if not found on self.
        Also wrap callables so they first switch to the correct tab.
        """
        driver = object.__getattribute__(self, "driver")
        attr = getattr(driver, name)
        if callable(attr) and not name.startswith("__"):
            @wraps(attr)
            def wrapped(*args, **kwargs):
                handle = object.__getattribute__(self, "handle")
                if driver.current_window_handle != handle:
                    driver.switch_to.window(handle)
                return attr(*args, **kwargs)
            return wrapped
        return attr


def setupDriver(
    webdriverPath: str = os.path.join(os.path.dirname(__file__), r"webdriver\chromedriver.exe"), 
    num_tabs: int = 1,
    options: list[str] = [],
    experimentalOptions: dict[str, any] = dict()
) -> list[TabDriver]:
    """
    Initializes a single Chrome instance with multiple tabs, then returns a list
    of TabDriver instances—one for each tab.
    """
    chrome_service = ChromeService(executable_path=webdriverPath)
    chrome_service.creation_flags = subprocess.CREATE_NO_WINDOW
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("log-level=3")

    for option in options:
        chrome_options.add_argument(option)
    
    chrome_options.add_experimental_option("prefs", experimentalOptions)
    
    driver = webdriver.Chrome(service=chrome_service, options=chrome_options)
    driver.maximize_window()

    # Open additional tabs
    for _ in range(num_tabs - 1):
        driver.execute_script("window.open('');")

    # Return one TabDriver per tab.
    return [TabDriver(driver, i) for i in range(num_tabs)]


def getCredenciais(id: int) -> tuple[str, str] | tuple[None, None]:
    """
    Recupera as credenciais (login e senha) de uma API com base no ID fornecido.

    Esta função faz uma requisição `GET` para uma API REST usando o ID fornecido e tenta recuperar as credenciais de login e senha. Se a requisição for bem-sucedida (status code 200) e os dados estiverem presentes, ela retorna uma tupla contendo o login e a senha. Caso contrário, retorna uma tupla com `None` nos dois valores.

    Args:
        id (int): O ID utilizado para buscar as credenciais na API.

    Returns:
        tuple[str, str] | tuple[None, None]: 
            - Uma tupla contendo `login` e `senha` se a requisição for bem-sucedida e os dados estiverem presentes.
            - Uma tupla `(None, None)` se a requisição falhar ou os dados não estiverem disponíveis.
    """
    url = f"http://172.16.10.6:8080/credenciais/{id}"
    try:
        resposta = requests.get(url)
        if resposta.status_code == 200:
            dados = resposta.json()
            login = dados.get('login')
            senha = dados.get('senha')
            return login, senha
        return None, None
    except Exception as e:
        print(e)
        print("Não foi possível acessar a API")


def instalarPacote(pacote: str):
    """
    Instala uma biblioteca do python
    Arguments:
        pacote: nome do pacote disponível no PyPI
    """
    subprocess.check_call([sys.executable, "-m", "pip", "install", pacote])
 
 
def getNumeroSolicitacao(virtaus: Chrome):
    time.sleep(5)

    urlAtual = virtaus.current_url
 
    parsed_url = urlparse(urlAtual)
    query_params = parse_qs(parsed_url.query)
 
    if 'app_ecm_workflowview_processInstanceId' in query_params:
        return query_params['app_ecm_workflowview_processInstanceId'][0]
    return None
 

def aguardarAlert(driver: Chrome) -> str:
    try:
        alert = WebDriverWait(driver, 10).until(EC.alert_is_present())
        alert_text = alert.text
        try:
            alert.accept()
        except:
            alert.dismiss()
        return alert_text
    except:
        return ""


def selectOption(driver: webdriver.Chrome, selectXpath: str, visibleText: str):
    select = Select(esperarElemento(driver, selectXpath))
    select.select_by_visible_text(visibleText)


def esperarElemento(driver: Chrome, xpath: str, tempo_espera=10, logLevel: int = 0):
    """
    Aguarda o elemento ser renderizado
    Arguments:
        driver: driver do site
        xpath: XPath do elemento
        tempo_espera: Tempo máximo de espera, em segundos
    Returns:
        Elemento
    """
    try:
        return WebDriverWait(driver, tempo_espera).until(EC.visibility_of_element_located(('xpath', xpath)))
    except:
        if logLevel:
            print(f"Elemento não encontrado: {xpath}")
 
 
def esperarElementos(driver: Chrome, xpath: str, tempo_espera=10) -> list[WebElement]:
    """
    Aguarda todos os elementos serem renderizados.
    Arguments:
        driver: driver do site
        xpath: XPath dos elementos
        tempo_espera: Tempo máximo de espera, em segundos
    Returns:
        Lista de elementos
    """
    try:
        return WebDriverWait(driver, tempo_espera).until(EC.presence_of_all_elements_located(('xpath', xpath)))
    except:
        return []
 

def clickarElemento(driver: Chrome, xpath: str, time_wait=10, logLevel: int = 0):
    """
    Retorna o elemento do Xpath de entrada
    Args:
        driver: driver do site
        xpath: XPath do elemento
    Returns:
        Elemento
    """
    try:
        return WebDriverWait(driver, time_wait).until(EC.element_to_be_clickable(('xpath', xpath)))
    except:
        if logLevel:
            print(f"Elemento não encontrado: {xpath}")


def clickElement(driver: Chrome, xpath: str, tempoEspera: int = 20):
    """
        Aguarda o elemento entrar em estado clicável e executa um clique usando Javascript
    """
    driver.execute_script("arguments[0].click();", WebDriverWait(driver, tempoEspera).until(EC.element_to_be_clickable((By.XPATH, xpath))))


def mensagemTelegram(token: str, chat_id: int, mensagem: str):
    """
    Envia uma mensagem pela API do Telegram
    Arguments:
        token: token do bot do Telegram
        chat_id: id do chat
        mensagem: mensagem a ser enviada
    Returns:
        JSON com a resposta da requisição
    """
    mensagem_formatada = f'https://api.telegram.org/bot{token}/sendMessage?chat_id={chat_id}&parse_mode=HTML&text={mensagem}'
    resposta = requests.get(mensagem_formatada)
    return resposta.json()
 
 
       
def esperar_elemento(driver: Chrome, xpath: str, tempo_espera=10):
    
    return WebDriverWait(driver, tempo_espera).until(EC.visibility_of_element_located(('xpath', xpath)))


def aguardarDownload(downloadsFolder: str, substringNomeArquivo: str, checkpoint: float = None) -> str:
    """
    Aguarda o download de arquivos contendo uma substring específica no nome após um determinado ponto de verificação, se fornecido.

    Args:
        downloadsFolder (str): Caminho do diretório de download.
        substringNomeArquivo (str): Substring que o arquivo baixado deve conter no nome.
        checkpoint (float, optional): Marca de tempo (timestamp) para verificar os arquivos baixados após esse momento. Se não fornecido, todos os arquivos serão verificados.

    Returns:
        str: Caminho completo do arquivo baixado, se encontrado.
    """

    if not os.path.exists(downloadsFolder):
        raise FileNotFoundError(f"A pasta de downloads não foi encontrada: {downloadsFolder}")

    if checkpoint is None:
        checkpoint = datetime.datetime.now().timestamp()

    while True:
        matchingArquivos = [arquivo for arquivo in os.listdir(downloadsFolder) if substringNomeArquivo in arquivo]
        
        for arquivo in matchingArquivos:
            caminhoArquivo = os.path.join(downloadsFolder, arquivo)
            data_modificacao = os.path.getmtime(caminhoArquivo)
            if (data_modificacao > checkpoint) and not arquivo.endswith(".crdownload"):
                return caminhoArquivo

        time.sleep(1)



def solveReCaptcha(driver):
    
    from selenium_recaptcha_solver import RecaptchaSolver
    
    ffmpeg_dir = os.path.join(os.path.dirname(__file__), "ffmpeg", "bin")
    ffmpeg_path = os.path.join(ffmpeg_dir, "ffmpeg.exe" if sys.platform == "win32" else "ffmpeg")

    os.environ["PATH"] = ffmpeg_dir + os.pathsep + os.environ["PATH"]

    solver = RecaptchaSolver(driver=driver)
    recaptcha_iframe = esperarElemento(driver, '//iframe[@title="reCAPTCHA"]')
    solver.click_recaptcha_v2(iframe=recaptcha_iframe)


def enviarCaptcha(imagePath: str | Path, enumBanco: EnumBanco, enumProcesso: EnumProcesso, token: str = TOKEN_CAPTCHA, chatId: str = CHAT_ID_CAPTCHA, tempoEspera: int = 45) -> str:
    """
    Envia uma imagem do captcha para um chat do Telegram e retorna uma resposta no intervalo de tempo.

    Args:
        chat_id (int): ID do chat do Telegram.
        imagePath (str | Path): Caminho da imagem do captcha.
    """

    baseUrl = f'https://api.telegram.org/bot{token}'
    
    if enumProcesso in [EnumProcesso.IMPORTACAO, EnumProcesso.APROVADORES]:
        chatId = "-1002257326271"

    formatName = lambda x: (" ".join(c for c in x.split('_'))).upper()

    with open(imagePath, 'rb') as imageFile:
        parametros = {
            "chat_id": chatId,
            "caption": f"Realizar Captcha\n{formatName(enumBanco.name)} {formatName(enumProcesso.name)}"
        }

        files = {
            "photo": imageFile
        }

        resp = requests.post(f"{baseUrl}/sendPhoto", data=parametros, files=files).json()
        messageId = resp["result"]["message_id"]

    time.sleep(tempoEspera)
    response = requests.get(f"{baseUrl}/getUpdates")
    updates = response.json()
    
    for update in reversed(updates.get("result", [])):
        if "message" in update:
            if "reply_to_message" in update["message"]:
                if update["message"]["reply_to_message"]["message_id"] == messageId:
                    return update["message"]["text"]
    
    return "123456"


def saveCaptchaImage(imgElement: WebElement, enumBanco: EnumBanco, enumProcesso: EnumProcesso):

    imgFolderPath = os.getcwd()
    imgName = f"Token_{enumBanco.name}_{enumProcesso.name}.png"
    
    imgPath = os.path.join(imgFolderPath, imgName)

    imgElement.screenshot(imgName)

    return imgPath


def clickCoordenada(driver: Chrome, x: int, y: int) -> None:
    """
    Clica em uma coordenada específica na tela.
    Args:
        driver: driver do site
        x: coordenada x
        y: coordenada y
    """

    action = ActionBuilder(driver)
    action.pointer_action.move_to_location(x, y)
    action.pointer_action.click()
    action.perform()
    

def importarPastaMonitoramento(filePathList: list[str], diretorioBase: str, data: datetime.datetime = None):
    try:
        if data:
            hoje = data
        else:
            hoje = datetime.datetime.now()
        pastaAno = str(hoje.year)
        pastaMes = f"{hoje.month:02d} - {meses[hoje.month]}"
        pastaDia = f"{hoje.day:02d}"
    
        caminho = os.path.join(diretorioBase, pastaAno, pastaMes, pastaDia)

        os.makedirs(caminho, exist_ok=True)

        for filePath in filePathList:
            
            nomeArquivo = os.path.basename(filePath)
            destino = os.path.join(caminho, nomeArquivo)

            shutil.copy(filePath, destino)
            os.remove(filePath)

        return caminho
    
    except Exception as e:
        print(e)


def coletarEmailEspecifico(email):
    CLIENT_ID = "d45fc956-3ea0-4c51-93be-c1ac46502c0d"
    CLIENT_SECRET = "oDm8Q~Wi2fH0fgc5xBqStZvBeAoDoKCwHjYyHbH0"
    TENANT_ID = "adaa0a29-8e4a-4216-8ac8-187b1608c2e1"
    USER_ID = email 
    AUTHORITY = f"https://login.microsoftonline.com/{TENANT_ID}"
    SCOPES = ["https://graph.microsoft.com/.default"]  # Escopo adequado para client credentials


    # Configuração do fluxo de autenticação
    app = msal.ConfidentialClientApplication(
        CLIENT_ID,
        authority=AUTHORITY,
        client_credential=CLIENT_SECRET
    )

    # Solicitando o token com o client_credentials flow
    result = app.acquire_token_for_client(scopes=SCOPES)

    if "access_token" in result:
        print("Token obtido com sucesso!")
        access_token = result["access_token"]
        headers = {"Authorization": f"Bearer {access_token}"}

        # Passo 1: Acessar as mensagens sem filtro ou ordenação
        messages_url = f"https://graph.microsoft.com/v1.0/users/{USER_ID}/messages?$top=20"  # Recupera os 20 e-mails mais recentes
        
        # Recuperando as mensagens
        messages_response = requests.get(messages_url, headers=headers)
        
        if messages_response.status_code == 200:
            result_data = messages_response.json()
            messages = result_data.get("value", [])
            
            # Filtrando as mensagens pelo assunto e ordenando pelo recebimento
            filtered_messages = [
                msg for msg in messages
                if "BemWeb - Pin Autenticação" in msg['subject']
            ]
            sorted_messages = sorted(filtered_messages, key=lambda x: x['receivedDateTime'], reverse=True)

            if sorted_messages:
                email = sorted_messages[0]  # Pegando o primeiro e-mail após a ordenação
                subject = email['subject']
                sender = email['from']['emailAddress']['address']
                print(f"Assunto: {subject}")
                print(f"De: {sender}")
                
                # Extraindo o corpo do e-mail
                email_body = email['body']['content']
                print(f"Corpo do e-mail: {email_body}\n")
                
                # Usando regex para extrair o PIN
                pin_match = re.search(r"seguida:<br><br><b>(\d+)</b>", email_body)
                if pin_match:
                    pin = pin_match.group(1)  # O número encontrado
                    print(f"PIN encontrado: {pin}")
                    return pin


def dataEscolha(days: int, formato: str = '%d/%m/%Y') -> str:
    return (datetime.datetime.today() - datetime.timedelta(days=days)).strftime(formato)


if __name__=="__main__":
    
    TOKEN = "8013361039:AAHvz0K-kW6SCNpk19nsGnBkCMGayc8zzbo"
    CHAT_ID = "-1002257326271"
    # imgPath = r"C:\Users\dannilo.costa\Pictures\Imagem1.png"
    # enviarCaptcha(imgPath, EnumBanco.BMG, EnumProcesso.IMPORTACAO, TOKEN, CHAT_ID)
    # user, senha = "1175.06433478522", "iren@06433"

    # loginCrefisaCP(driver, user, senha)

    google, github, stack = setupDriver(num_tabs=3)
    google.get("https://www.google.com")
    github.get("https://www.github.com")
    stack.get("https://www.stackoverflow.com")
    
    print(github.current_url)

    input("...")