import os
import time
import inspect
from time import sleep
from functools import wraps
from typing import Callable
from Adlib.api import *
from Adlib.funcoes import *
from selenium.webdriver import Chrome
from selenium.webdriver.common.keys import Keys


token = "7505814396:AAHQvtr0ltePOLKp88awG7WHB6lksKkNaR0"
chatId = "-4095757991"

formatEnumName = lambda x: x.name.replace('_', ' ')


class LoginReturn(Enum):
    ACESSO_SIMULTANEO = "Acesso simultâneo"
    CAPTCHA_INCORRETO = "Captcha incorreto"
    LOGIN_COM_SUCESSO = "Login com sucesso"
    CREDENCIAIS_INVALIDAS = "Credenciais inválidas"
    USUARIO_INATIVO = "Usuário inativo"
    ERRO_AO_LOGAR = "Erro ao logar"
    RESETAR_SENHA = "Resetar senha"
    ATUALIZAR_DADOS = "Atualizar Dados Cadastrais"


def login_decorator(func):

    def loginFunctionPrototype(driver: Chrome, usuario: str, senha: str) -> LoginReturn:
        pass


    def loginCaptchaFunctionPrototype(driver: Chrome, usuario: str, senha: str, enumProcesso: EnumProcesso) -> tuple[LoginReturn, str, str, EnumBanco]:
        pass


    loginFunctionModel = inspect.signature(loginFunctionPrototype)
    loginCaptchFunctionModel = inspect.signature(loginCaptchaFunctionPrototype)

    def validateLoginFunction(func: Callable) -> bool:
        funcSignature = inspect.signature(func)
        if funcSignature not in [loginFunctionModel, loginCaptchFunctionModel]:
            raise TypeError(
                f"A função {func.__name__} não está no formato adequado!\
                \n{loginFunctionModel}\
                \n{loginCaptchFunctionModel}"
            )
        return True

    @wraps(func)
    def wrapper(driver: Chrome, usuario: str, senha: str, *args):
        isValidLoginFunction = validateLoginFunction(func)
        if isValidLoginFunction:
            try:
                loginReturn: LoginReturn = func(driver, usuario, senha, *args)
                print(loginReturn)
                if loginReturn != LoginReturn.LOGIN_COM_SUCESSO:
                    mensagemTelegram(token, chatId, f"{loginReturn.value} | {func.__name__}")

            except Exception as e:
                print(f"Erro ao realizar login: {func.__name__}")
                print(e)
            sleep(10)
    return wrapper


def captcha_decorator(loginFunc: Callable[[Chrome, str, str, EnumProcesso], tuple[LoginReturn, str, str, EnumBanco]]) -> LoginReturn:
    @wraps(loginFunc)
    def wrapper(driver: Chrome, usuario: str, senha: str, enumProcesso: EnumProcesso) -> tuple[LoginReturn, str, str]:
        while True:
            loginReturn, imgPath, captcha, enumBanco = loginFunc(driver, usuario, senha, enumProcesso)
            
            print(loginReturn)
            if enumProcesso in [EnumProcesso.IMPORTACAO, EnumProcesso.APROVADORES]:
                global chatId
                chatId = "-1002257326271"

            if enumProcesso in [EnumProcesso.CONFIRMACAO_CREDITO]:
                pass

            if loginReturn != LoginReturn.CAPTCHA_INCORRETO:
                timestamp = int(time.time())
                novo_nome = f"{timestamp}_{captcha}.png"
                novo_caminho = os.path.join(os.path.dirname(imgPath), novo_nome)
                
                os.rename(imgPath, novo_caminho)
                
                try:
                    storeCaptcha(novo_caminho, enumBanco, enumProcesso)
                except Exception as e:
                    os.remove(novo_caminho)
                    print(e)
                
                if loginReturn == LoginReturn.RESETAR_SENHA:
                    input("Resetar a senha")
                if loginReturn != LoginReturn.ACESSO_SIMULTANEO:
                    return loginReturn
            
            os.remove(imgPath)

            aguardarAlert(driver)
            driver.refresh()
            aguardarAlert(driver)

    return wrapper


@login_decorator
def loginItau(driver: Chrome, usuario: str, senha: str) -> LoginReturn:
    
    def checkLogin() -> LoginReturn:
        if driver.current_url == "https://portal.icconsig.com.br/proposal":
            return LoginReturn.LOGIN_COM_SUCESSO

    driver.get('https://portal.icconsig.com.br/')
    sleep(10)

    iframe = esperarElemento(driver, '/html/body/cc-lib-dialog/div/div[1]/div[2]/div/app-auth-dialog/div/iframe', tempo_espera=20)
    driver.switch_to.frame(iframe)

    esperarElemento(driver, '//*[@id="username"]').send_keys(usuario)
    esperarElemento(driver, '//*[@id="password"]').send_keys(senha + Keys.ENTER)
    
    return checkLogin()

@login_decorator
def loginCrefisaCP(driver: Chrome, usuario: str, senha: str) -> LoginReturn:

    driver.get("https://app1.gerencialcredito.com.br/CREFISA/default.asp")

    esperarElemento(driver, '//*[@id="txtUsuario"]').send_keys(usuario)
    esperarElemento(driver, '//*[@id="txtSenha"]').send_keys(senha)

    solveReCaptcha(driver)
    esperarElemento(driver, '//*[@id="btnLogin"]').click()
    
    return LoginReturn.LOGIN_COM_SUCESSO

@login_decorator
def loginC6(driver: Chrome, usuario: str, senha: str) -> LoginReturn:

    def checkLogin() -> LoginReturn:
        text = aguardarAlert(driver)

        if "Usuário ou senha inválido" in text:
            return LoginReturn.CREDENCIAIS_INVALIDAS
        if "Usuário inativo ou afastado" in text:
            return LoginReturn.USUARIO_INATIVO
        if "Usuário já autenticado" in text:
            return LoginReturn.LOGIN_COM_SUCESSO
        if esperarElemento(driver, '//span[contains(text(), "Atualizar meus Dados Cadastrais")]', tempo_espera=3):
            return LoginReturn.ATUALIZAR_DADOS
        LoginReturn.ERRO_AO_LOGAR


    driver.get("https://c6.c6consig.com.br/WebAutorizador/Login/AC.UI.LOGIN.aspx")

    esperarElemento(driver, "//*[@id='EUsuario_CAMPO']").send_keys(usuario)
    esperarElemento(driver, "//*[@id='ESenha_CAMPO']").send_keys(senha)
    clickarElemento(driver, '//*[@id="lnkEntrar"]').click()

    return checkLogin()
    

@login_decorator
def loginDigio(driver: Chrome, usuario: str, senha: str) -> LoginReturn:

    def checkLogin() -> LoginReturn:
        text = aguardarAlert(driver)
        
        if "Usuário ou senha inválido" in text:
            return LoginReturn.CREDENCIAIS_INVALIDAS
        if "Usuário inativo ou afastado" in text:
            return LoginReturn.USUARIO_INATIVO
        if "Usuário já autenticado" in text:
            return LoginReturn.LOGIN_COM_SUCESSO
        if esperarElemento(driver, '//span[contains(text(), "Alteração de Senha")]', tempo_espera=3):
            return LoginReturn.RESETAR_SENHA
        if esperarElemento(driver, '//span[contains(text(), "Atualizar meus Dados Cadastrais")]', tempo_espera=3):
            return LoginReturn.ATUALIZAR_DADOS
            
        LoginReturn.ERRO_AO_LOGAR

    driver.get("https://funcaoconsig.digio.com.br/FIMENU/Login/AC.UI.LOGIN.aspx")

    esperarElemento(driver, "//*[@id='EUsuario_CAMPO']").send_keys(usuario)
    esperarElemento(driver, "//*[@id='ESenha_CAMPO']").send_keys(senha)
    clickarElemento(driver, '//*[@id="lnkEntrar"]').click()
    
    return checkLogin()


@login_decorator
def loginBlip(driver: Chrome, usuario: str, senha: str) -> LoginReturn:

    driver.get('https://takegarage-7ah6a.desk.blip.ai/')
    sleep(5)
    shadowPrincipal = driver.find_element('css selector', 'body > bds-theme-provider > bds-grid > bds-grid.form_space.host.direction--undefined.justify_content--center.flex_wrap--undefined.align_items--center.xxs--12.xs--undefined.sm--undefined.md--6.lg--undefined.xg--undefined.gap--undefined.xxsoffset--undefined.xsoffset--undefined.smoffset--undefined.mdoffset--undefined.lgoffset--undefined.xgoffset--undefined.padding--undefined.margin--undefined.hydrated > bds-grid.login-content.host.direction--column.justify_content--undefined.flex_wrap--undefined.align_items--undefined.xxs--10.xs--6.sm--undefined.md--6.lg--undefined.xg--undefined.gap--2.xxsoffset--undefined.xsoffset--undefined.smoffset--undefined.mdoffset--1.lgoffset--undefined.xgoffset--undefined.padding--undefined.margin--undefined.hydrated > bds-grid.host.direction--column.justify_content--undefined.flex_wrap--undefined.align_items--undefined.xxs--undefined.xs--undefined.sm--undefined.md--undefined.lg--undefined.xg--undefined.gap--2.xxsoffset--undefined.xsoffset--undefined.smoffset--undefined.mdoffset--undefined.lgoffset--undefined.xgoffset--undefined.padding--undefined.margin--undefined.hydrated')
    shadow_root = driver.execute_script("return arguments[0].shadowRoot", shadowPrincipal)

    shadow_host = driver.find_element('css selector', '#email-input')
    shadow_root = driver.execute_script("return arguments[0].shadowRoot", shadow_host)
    shadow_root.find_element('class name', 'input__container__text').send_keys(usuario)

    # Shadow host Senha
    shadow_host = driver.find_element('css selector', '#password-input')
    shadow_root = driver.execute_script("return arguments[0].shadowRoot", shadow_host)
    shadow_root.find_element('css selector', 'div > div.input__container > div > input').send_keys(senha + Keys.ENTER + Keys.ENTER)
    sleep(5)


@login_decorator
def loginFacta(driver: Chrome, usuario: str, senha: str) -> LoginReturn:

    def checkLogin() -> LoginReturn:
        if esperarElemento(driver, '//*[@id="divAlertaMsg"][contains(text(), "SUA SENHA PRECISA SER ALTERADA!")]', tempo_espera=3):
            return LoginReturn.RESETAR_SENHA
        if driver.current_url == "https://desenv.facta.com.br/sistemaNovo/dashboard.php":
            return LoginReturn.LOGIN_COM_SUCESSO
        
        return LoginReturn.ERRO_AO_LOGAR
    
    driver.get('https://desenv.facta.com.br/sistemaNovo/login.php')
    
    esperarElemento(driver, '//*[@id="login"]').send_keys(usuario)
    esperarElemento(driver, '//*[@id="senha"]').send_keys(senha)

    esperarElemento(driver,'//*[@id="btnLogin"]').click()

    return checkLogin()


@login_decorator
def loginMargem(driver: Chrome, usuario: str, senha: str) -> LoginReturn:
    driver.get('https://adpromotora.promobank.com.br/') 

    esperarElemento(driver, '//*[@id="inputUsuario"]').send_keys(usuario)
    esperarElemento(driver, '//*[@id="passField"]').send_keys(senha + Keys.ENTER)

    return LoginReturn.LOGIN_COM_SUCESSO


def loginBanrisul(driver: Chrome, usuario: str, senha: str, email: str):
    driver.get('https://bemweb.bempromotora.com.br/autenticacao/login')

    esperarElemento(driver, '/html/body/main/div/div/div[2]/div[2]/form/div[1]/div[2]/div/span/input').send_keys(usuario)
    esperarElemento(driver, '/html/body/main/div/div/div[2]/div[2]/form/div[2]/button').click()
    time.sleep(5)

    esperarElemento(driver, '//*[@id="senha"]').send_keys(senha)
    esperarElemento(driver, '//*[@id="btn-login"]').click()
    
    try:
        time.sleep(10)
        pop_up = esperarElemento(driver, '/html/body/section[2]/div/button').click()

        time.sleep(4)         
    except:
        while True:
            pin = coletarEmailEspecifico(email)
            try:
                inputPIN = esperarElemento(driver, '//*[@id="pin"]').send_keys(pin + Keys.ENTER)
                time.sleep(10)
                pop_up = esperarElemento(driver, '/html/body/section[2]/div/button').click()
                time.sleep(4)
                return LoginReturn.LOGIN_COM_SUCESSO
            except:
                inputPIN = esperarElemento(driver, '//*[@id="pin"]').clear()
                print('Tente logar novamente')


@login_decorator
def loginCashCard(driver: Chrome, usuario: str, senha: str) -> LoginReturn:
    
    driver.get(f"https://front.meucashcard.com.br/WebAppBPOCartao/Login/ICLogin?ReturnUrl=%2FWebAppBPOCartao%2FPages%2FProposta%2FICPropostaCartao")
     
    esperarElemento(driver, '//*[@id="txtUsuario_CAMPO"]').send_keys(usuario)
    esperarElemento(driver, '//*[@id="txtSenha_CAMPO"]').send_keys(senha)

    esperarElemento(driver, '//*[@id="bbConfirmar"]').click()

    return LoginReturn.LOGIN_COM_SUCESSO


@login_decorator
def loginVirtaus(driver: Chrome, usuario: str, senha: str) -> LoginReturn:
    driver.get("https://app.fluigidentity.com/ui/login")
    sleep(5)

    esperarElemento(driver, '//*[@id="username"]').send_keys(usuario)
    esperarElemento(driver, '//*[@id="password"]').send_keys(senha + Keys.ENTER)
    
    return LoginReturn.LOGIN_COM_SUCESSO


@login_decorator
def loginPaulista(driver: Chrome, usuario: str, senha: str) -> LoginReturn:
    driver.get("https://creditmanager.bancopaulista.com.br/Login.aspx?ReturnUrl=%2fConcessao%2fMonitor.aspx")
    
    esperarElemento(driver, '//*[@id="MainContent_txtUsuario"]').send_keys(usuario)
    esperarElemento(driver, '//*[@id="MainContent_txtSenha"]').send_keys(senha)
    
    esperarElemento(driver, '//*[@id="MainContent_Button1"]').click()
    
    return LoginReturn.LOGIN_COM_SUCESSO


@login_decorator
def loginSafra(driver: Chrome, usuario: str, senha: str):
    driver.get("https://epfweb.safra.com.br/")
    
    esperarElemento(driver, '//*[@id="txtUsuario"]').send_keys(usuario)
    esperarElemento(driver, '//*[@id="txtSenha"]').send_keys(senha + Keys.ENTER)
    sleep(35)
    try:
        buttonLogin = esperarElemento(driver, '//*[@id="btnEntrar"]')
        buttonLogin.click()
    finally:
        sleep(5)

    
@login_decorator
def loginMaster(driver: Chrome, usuario: str, senha: str) -> LoginReturn:
    
    driver.get('https://autenticacao.bancomaster.com.br/login')

    esperarElemento(driver, '//*[@id="mat-input-0"]').send_keys(usuario)
    esperarElemento(driver, '//*[@id="mat-input-1"]').send_keys(senha)
    clickarElemento(driver, '/html/body/app-root/app-login/div/div[2]/mat-card/mat-card-content/form/div[3]/button[2]').click()
    try:
        clickarElemento(driver, '//*[@id="mat-dialog-0"]/app-confirmacao-dialog/div/div[3]/div/app-botao-icon-v2[2]/button').click()
    except:
        pass

    return LoginReturn.LOGIN_COM_SUCESSO



@login_decorator
@captcha_decorator
def loginIBConsig(driver: Chrome, usuario: str, senha: str, enumProcesso: EnumProcesso) -> tuple[LoginReturn, str, str, EnumBanco]:
    
    enumBanco = EnumBanco.ITAU

    def checkLogin() -> LoginReturn:
        if esperarElemento(driver, '//*[@id="Table_01"]//font[contains(normalize-space(text()), "Usuário e/ou senha inválido")]', tempo_espera=3):
            return LoginReturn.CREDENCIAIS_INVALIDAS
        if driver.current_url == "https://www.ibconsigweb.com.br/principal/fsconsignataria.jsp":
            return LoginReturn.LOGIN_COM_SUCESSO
        
        return LoginReturn.ERRO_AO_LOGAR
    
    driver.get("https://www.ibconsigweb.com.br/")

    esperarElemento(driver, '/html/body/table/tbody/tr[2]/td[3]/table/tbody/tr/td/form/table/tbody/tr[1]/td[3]/input').send_keys(usuario)
    esperarElemento(driver, '/html/body/table/tbody/tr[2]/td[3]/table/tbody/tr/td/form/table/tbody/tr[2]/td[2]/font/strong/input').send_keys(senha)
                                     
    captchaElement = esperarElemento(driver, '/html/body/table/tbody/tr[2]/td[3]/table/tbody/tr/td/form/table/tbody/tr[4]/td/table/tbody/tr[2]/td/iframe')

    imgPath = saveCaptchaImage(captchaElement, enumBanco, enumProcesso)

    captcha = enviarCaptcha(imgPath, enumBanco, enumProcesso)

    try:
        esperarElemento(driver, '/html/body/table/tbody/tr[2]/td[3]/table/tbody/tr/td/form/table/tbody/tr[4]/td/table/tbody/tr[1]/td[2]/input').send_keys(captcha)

        esperarElemento(driver, '/html/body/table/tbody/tr[2]/td[3]/table/tbody/tr/td/form/table/tbody/tr[4]/td/table/tbody/tr[1]/td[3]/a').click()
        sleep(10)
    except Exception as e:
        print(e)
        
    if loginReturn:=checkLogin():
        mensagemTelegram(token, chatId, f"Entrou! {formatEnumName(enumBanco)} {formatEnumName(enumProcesso)} ✅")

    return loginReturn, imgPath, captcha, enumBanco


@login_decorator
@captcha_decorator
def loginBMG(driver: Chrome, usuario: str, senha: str, enumProcesso: EnumProcesso) -> tuple[LoginReturn, str, str, EnumBanco]:
    
    def fecharAbasPopUp():
        substring = "bmgconsig"
        originalTab = driver.current_window_handle

        popups = [handle for handle in driver.window_handles if handle != originalTab]

        for handle in popups:
            driver.switch_to.window(handle)
            if substring in driver.current_url:
                driver.close()

        driver.switch_to.window(originalTab)

    def checkLoginBMG() -> LoginReturn:

        if esperarElemento(driver, '//*[@id="div-error"]/span[contains(text(), "A palavra de verificação está inválida.")]', tempo_espera=3):
            return LoginReturn.CAPTCHA_INCORRETO
        
        if esperarElemento(driver, '//*[@id="div-error"]/span[contains(text(), "Usuário/Senha inválidos")]', tempo_espera=3):
            return LoginReturn.CREDENCIAIS_INVALIDAS
        
        if esperarElemento(driver, '//*[@id="div-error"]/span[contains(text(), "Usuário se encontra bloqueado")]', tempo_espera=3):
            return LoginReturn.USUARIO_INATIVO

        if esperarElemento(driver, '//*[@id="div-error"]/span[contains(text(), "tentativa de acesso simultâneo")]', tempo_espera=3):
            return LoginReturn.ACESSO_SIMULTANEO
        
        driver.switch_to.frame(esperarElemento(driver, '//*[@id="rightFrame"]'))

        if esperarElemento(driver, '//font[contains(text(), "A sua senha expirou")]', tempo_espera=3):
            return LoginReturn.RESETAR_SENHA
        
        driver.switch_to.default_content()
        
        if driver.current_url == "https://www.bmgconsig.com.br/principal/fsconsignataria.jsp":
            return LoginReturn.LOGIN_COM_SUCESSO
        
        return LoginReturn.ERRO_AO_LOGAR
    
    enumBanco = EnumBanco.BMG
    
    driver.get("https://www.bmgconsig.com.br/Index.do?method=prepare")

    esperarElemento(driver,'//*[@id="usuario"]').send_keys(usuario + Keys.ENTER)
    esperarElemento(driver, '//*[@id="j_password"]').send_keys(senha + Keys.ENTER)

    captchaElement = esperarElemento(driver, '/html/body/section[1]/div/div[1]/div/div/form/div[3]/iframe')

    imgPath = saveCaptchaImage(captchaElement, enumBanco, enumProcesso)

    captcha = enviarCaptcha(imgPath, enumBanco, enumProcesso)
    try:
        esperarElemento(driver, '//*[@id="captcha"]').send_keys(captcha)

        esperarElemento(driver, '//*[@id="bt-login"]').click()
        sleep(10)
    except Exception as e:
        print(e)

    loginReturn = checkLoginBMG()

    if loginReturn == LoginReturn.LOGIN_COM_SUCESSO:
        fecharAbasPopUp()
        mensagemTelegram(token, chatId, f"Entrou! {formatEnumName(enumBanco)} {formatEnumName(enumProcesso)} ✅")

    return loginReturn, imgPath, captcha, enumBanco


@login_decorator
@captcha_decorator
def loginDaycoval(driver: Chrome, usuario: str, senha: str, enumProcesso: EnumProcesso) -> tuple[LoginReturn, str, str, EnumBanco]:

    enumBanco = EnumBanco.DAYCOVAL

    def checkLogin():
        text = aguardarAlert(driver)

        if "Código da Imagem Inválido" in text:
            return LoginReturn.CAPTCHA_INCORRETO
        
        if "Usuário ou senha inválido" in text:
            return LoginReturn.CREDENCIAIS_INVALIDAS
        
        if "expirar" in text:
            return LoginReturn.RESETAR_SENHA
        
        if driver.current_url == "https://consignado.daycoval.com.br/Autorizador/": # URL após login bem sucedido
            return LoginReturn.LOGIN_COM_SUCESSO
        
        return LoginReturn.ERRO_AO_LOGAR
    
    aguardarAlert(driver)

    driver.get('https://consignado.daycoval.com.br/Autorizador/Login/AC.UI.LOGIN.aspx')
    sleep(5)
    
    esperarElemento(driver, '//*[@id="Captcha_lkReGera"]').click()
    sleep(1)
    esperarElemento(driver, '//*[@id="EUsuario_CAMPO"]').send_keys(usuario)
    esperarElemento(driver, '//*[@id="ESenha_CAMPO"]').send_keys(senha)
    
    captchaElement = driver.find_element('xpath', '//*[@id="form1"]/img')#captchaElement = esperarElemento(driver, '//*[@id="form1"]/img')

    imgPath = saveCaptchaImage(captchaElement, enumBanco, enumProcesso)

    captcha = enviarCaptcha(imgPath, enumBanco, enumProcesso)
    
    esperarElemento(driver, '//*[@id="Captcha_txtCaptcha_CAMPO"]').send_keys(captcha)

    esperarElemento(driver, '//*[@id="lnkEntrar"]').click()
    sleep(5)
    
    loginReturn = checkLogin()

    if loginReturn == LoginReturn.LOGIN_COM_SUCESSO:
        mensagemTelegram(token, chatId, f"Entrou! {formatEnumName(enumBanco)} {formatEnumName(enumProcesso)} ✅")

    return loginReturn, imgPath, captcha, enumBanco


def logoutBMG(bmg: Chrome):
    
    bmg.get("https://www.bmgconsig.com.br/login/logout.jsp")
    try:
        esperarElemento(bmg, '//*[@id="buttonLink"]').click()
        time.sleep(3)
        aguardarAlert(bmg)
    except:
        pass
    time.sleep(5)

def loginOle(driver: Chrome, usuario: str, senha: str) -> LoginReturn: 
    driver.get('https://ola.oleconsignado.com.br/')
    esperarElemento(driver, '//*[@id="Login"]').send_keys(usuario)
    esperarElemento(driver, '//*[@id="Senha"]').send_keys(senha + Keys.ENTER)
    
    esperarElemento(driver, '//*[@id="botaoAcessar"]').click()

    return LoginReturn.LOGIN_COM_SUCESSO


@login_decorator
def loginOle(driver: Chrome, usuario: str, senha: str) -> LoginReturn: 
    driver.get('https://ola.oleconsignado.com.br/')
    esperarElemento(driver, '//*[@id="Login"]').send_keys(usuario)
    esperarElemento(driver, '//*[@id="Senha"]').send_keys(senha + Keys.ENTER)
    
    esperarElemento(driver, '//*[@id="botaoAcessar"]').click()

    return LoginReturn.LOGIN_COM_SUCESSO


if __name__=="__main__":

    options = [
        "--disable-blink-features=AutomationControlled",
        "--disable-popup-blocking",
        "--no-sandbox",
        "--disable-dev-shm-usage",
        "--disable-software-rasterizer",
        "--lang=pt-BR",
        "--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    ]

    driver = setupDriver(
        options=options,
    )

    #loginBanco, senhaBanco = 
    user, senha = "SE07547063543A", "G@O1987Ts"#getCredenciais(409)
    
    # loginBMG(driver, user, senha, EnumProcesso.CONFIRMACAO_CREDITO)

    loginOle(driver, user, senha)

    input("FECHAR????")
    input("FECHAR????")
    input("FECHAR????")
    input("FECHAR????")
    input("FECHAR????")