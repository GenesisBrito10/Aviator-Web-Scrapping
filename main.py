
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


class Aviator:

    def __init__(self):

        self.options = webdriver.ChromeOptions()
        self.options.add_argument('--headless')
        self.options.add_argument('--disable-gpu')
        self.options.add_argument('--start-minimized')
        self.options.add_argument("--disable-infobars")
        self.options.add_argument("--disable-logging")
        self.options.add_argument("--disable-login-animations")
        self.options.add_argument("--disable-notifications")
        self.options.add_argument("--disable-default-apps")
        self.options.add_argument("--disable-popup-blocking")
        self.options.add_argument('--no-sandbox')
        self.options.add_argument('--force-device-scale-factor=0.8')

        self.url = "https://odin.sportingtech.com/api/user/login"
        self.payloadLogin = {
            'requestBody':{
            'username': " ", 
            'email': 'null', 
            'phone': 'null', 
            'keepLoggedIn': 'null', 
            'password': "", 
            'loginType': '1',
            }
            
        }

        self.headersLogin = {
            
            "Content-Type": "application/json",
            "Origin": "https://m.estrelabet.com",
            "Referer": "https://m.estrelabet.com/",
        }

        
        self.urlevo= 'https://odin.sportingtech.com/api/user/casinoapi/openGame'



    def initialize_browser(self):
        self.driver = webdriver.Chrome(
            options=self.options)
        return self.driver

    def pegar_resultado(self):
        
        wait = WebDriverWait(self.driver, 10)
        wait.until(EC.visibility_of_element_located(
                (By.CSS_SELECTOR, ".payouts-block")))
        
        elements = self.driver.find_elements(
            By.CLASS_NAME, "payouts")

        # Lê os textos de cada elemento e os armazena em uma lista
        multipliers = []
        for element in elements[:10]:
            try:
                multiplier = float(element.text.replace('x', ''))
                multipliers.append(multiplier)
            except ValueError:
                pass

        return multipliers

    def start(self):

        with requests.session() as session:

            response = session.post(self.url, json=self.payloadLogin, headers=self.headersLogin)


            if response.status_code == 200:
                print("Login bem-sucedido!")
                dados = response.json()
                traderId = dados['data']['traderId']
                pgUser = dados['data']['code']
                s7oryO9STV = response.headers.get('s7oryO9STV')
                
                headersEvo = {
            
            "Content-Type": "application/json",
            "Origin": "https://m.estrelabet.com",
            "Referer": "https://m.estrelabet.com/",
            "s7oryO9STV" : s7oryO9STV,
            "X-Pgdevice": "d",
            "X-Pgtradername": str(traderId),
            "X-Pgusername":pgUser,

        }
               
                payloadEvo = {
                    "requestBody": {
                        "gameId": "7787",
                        "channel": "web",
                        "vendorId": 78,
                        "redirectUrl": "https://estrelabet.com/en/games/casino/detail/normal/7787"
                    },
                    "identity": None,
                    "device": "d",
                    "languageId": 2
                }
                
                response2 = session.post(self.urlevo, json=payloadEvo, headers=headersEvo)
                data = response2.json()
                url = data['data']['gameUrl']
                response3 = session.get(url,json={
                    "redirect":"manual",
                })
                #print(response3.url)
                u = response3.url.split('?')[1]
                print(u)
                urljogo = f"https://aviator-next.spribegaming.com/?{u}"
                response = requests.post(urljogo)
                driver = self.initialize_browser()
                driver.get(urljogo)
                wait = WebDriverWait(self.driver, 10)
                wait.until(EC.visibility_of_element_located(
                (By.XPATH, "/html/body/app-root/app-game/div/div[1]/div[2]/div/div[2]/div[1]/app-stats-widget/div/div[3]/div"))).click()
                check = []
                while True:
                    results = []
                    results = self.pegar_resultado()
                    if check != results:
                        check = results
                        print(results)

            else:
                print("Falha no login. Código de status:", response.status_code)

app = Aviator().start()