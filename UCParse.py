import requests
import json
from bs4 import BeautifulSoup as BS
import time
import sys
from requests.packages.urllib3.exceptions import InsecureRequestWarning

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

class SessionUC:
    
    def __init__(self, username, password):
        self.__username = username
        self.__password = password
        self.session = requests.Session()
        self.token = None
        self.promocode = None

        self.payload = {
            'login': self.__username,
            'password': self.__password,
            'remember': 1,
            '_xfRedirect': '',
        }

    def auth(self):
        r_auth = self.session.post('https://uc.zone/login/login', data=self.payload, verify=False)
        token_bs = BS(r_auth.text, 'html.parser')
        try:
            self.token = token_bs.select('input[name=_xfToken]')[0]['value']
        except IndexError as e:
            print("Check email and confirm account..or shit happend")
        return r_auth

    def wait_new_promo(self):
        try:
            while True:
                time.sleep(3)
                promo_html = self.session.get('https://uc.zone/cheat-statuses/games/DotA2/load-promocode')
                promo_bs = BS(promo_html.content, 'html.parser')
             
                current_promocode = promo_bs.select('.gamePromocodeItem.gamePromocode--promocode')[0].text.strip()
                print(current_promocode)

                if promo_bs.select('.is-not-activated'):
                    self.promocode = promo_bs.select('.gamePromocodeItem.gamePromocode--promocode.is-not-activated')[0]\
                        .text.strip()
                    break
        except Exception as e:
            current_promocode = promo_bs.select('.gamePromocode.gamePromocode--empty')[0].text.strip()
            print(current_promocode)
            return False
            

    def activate_promo(self):
        promo_payload = {
            'promocode': self.promocode,
            '_xfToken': self.token
        }
        print(promo_payload)

        promo_req = self.session.post('https://uc.zone/account/promocode', data=promo_payload)
        html_returned = BS(promo_req.content, 'html.parser')

        #os.system('play --no-show-progress --null --channels 2 synth %s sine %f' %( 0.2, 400))
        return html_returned.select('.p-body-pageContent')[0].text.strip()


if __name__ == '__main__':
    
    se = SessionUC(input("Enter username:"), input("Enter password:"))

    login_result = se.auth()
    print(login_result.url)
    print(login_result.history)
    if not login_result.history:
        print("Invalid email or password")
        sys.exit()

    print(se.token)

    print('Waiting new promo')
    if se.wait_new_promo():
        print('Activating promocode')
        activate_result = se.activate_promo()

        print(activate_result)





