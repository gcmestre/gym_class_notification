# coding: utf-8

import requests
import configparser
from bs4 import BeautifulSoup

input_form_url = 'https://pump-spirit.com/my-pump/public_html/login'

no_class_available_text = "Não há aulas disponíveis para marcação."

club_id = {"faro": 87}

cookies = None


class Pump:

    def __init__(self, *args, **kwargs):

        self._read_config_file()

        self.cookies = None

    def _read_config_file(self):
        """
            Opens and reads the config file
        :return:
        """
        self.config = configparser.ConfigParser()
        self.config.read('config.cfg')

    def _config_get_username(self):
        print(self.config)
        return self.config['credentials']['username']

    def _config_get_password(self):
        return self.config['credentials']['password']

    def login(self):
        """
            Login into pump.
            Sets Cookies
        :return:
        """

        login_credentials = self._get_login_credetials()
        login_form_token = self._get_login_form_token()

        login_data = {
            "form[username]": login_credentials["username"],
            "form[password]": login_credentials["password"],
            "form[_token]": login_form_token
        }

        # Exepeted formation of the login data
        # login_form = {
        #     "form[username]": user email,
        #     "form[password]": password,
        #     "form[_token]": Hash of the form token
        # }

        login_page_response = requests.post('https://pump-spirit.com/my-pump/public_html/login',
                                            data=login_data,
                                            cookies=self.cookies)

        return login_page_response


    def _get_login_credetials(self):
        return {
            "username": self._config_get_username(),
            "password": self._config_get_password()
        }


    def _get_login_form_token(self):

        login_page = self.get_login_page()
        login_page_parsed = self._html_parsing(login_page.text)
        login_page_input_fields = self._get_input_fields_from_page(login_page_parsed)

        if login_page_input_fields[-1]['id'] != "form__token":
            print("Exeption('Error getting the login form field token')")
            #raise Exeption("Error getting the login form field token")

        return login_page_input_fields[-1]['value']


    def _html_parsing(self, html_page):
        return BeautifulSoup(html_page, 'html.parser')

    def _get_input_fields_from_page(selfs, html_page):
        return html_page.find_all('input')

    def get_login_page(self):
        """
            Posts a request of the login page
        :return:
        """
        login_page_response = requests.post('https://pump-spirit.com/my-pump/public_html/login', cookies=self.cookies)

        #TODO check a better way to check if the response as cookies or not
        if "PHPSESSID" in login_page_response.cookies:
            self.cookies = login_page_response.cookies

        return login_page_response

    def is_loggedin(self):

        login_page = self.get_login_page()

        return not ('id="form-register"' in login_page.text)



def is_class_available(html):
    return no_class_available_text in html

def is_logged_in(html):
    return not ('id="form-register"' in html)


def get_input_fields_from_page (html_page):

    return html_page.find_all('input')

def get_classes_from_page (html_page):

    return html_page.findAll("div", {"class": "mypump-class-wrapper"})

def get_reservation_page():
    reservation_page_response = requests.post('https://pump-spirit.com/my-pump/public_html/reservar', cookies=cookies)
    return reservation_page_response


def generate_reservation_dict():

    reservation_page = get_reservation_page()

    if not is_logged_in(reservation_page.text):
        login()

    reservation_login_page = html_parsing(reservation_page.text)

    reservation_input_fields = get_input_fields_from_page(reservation_login_page)

    reservation_form = {
        "form[clubsSimple]": club_id['faro'],
        "form[_token]":reservation_input_fields[-1]['value']
    }

    return reservation_form

def submit_login_form(login_form_data):

    login_page_response = requests.post('https://pump-spirit.com/my-pump/public_html/login',data=login_form_data, cookies=cookies)

    return login_page_response

def submit_reservation_form(reservation_form_data):

    login_page_response = requests.post('https://pump-spirit.com/my-pump/public_html/reservar',data=reservation_form_data, cookies=cookies)

    return login_page_response

def login():
    login_form_data = generate_login_dict()
    return submit_login_form(login_form_data)


if __name__ == '__main__':

    pump = Pump()

    print(pump.is_loggedin())

    pump.login()

    print(pump.is_loggedin())

