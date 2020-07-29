import requests
import configparser
from bs4 import BeautifulSoup
from pump_class import PumpClass

input_form_url = 'https://pump-spirit.com/my-pump/public_html/login'


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

    def _get_form_token(self, html_page):

        html_page_parsed = self._html_parsing(html_page.text)
        html_page_input_fields = self._get_input_fields_from_page(html_page_parsed)

        if html_page_input_fields[-1]['id'] != "form__token":
            print("Exeption('Error getting the form field token')")
            #raise Exeption("Error getting the login form field token")

        return html_page_input_fields[-1]['value']

    def _get_login_form_token(self):

        return self._get_form_token(self.get_login_page())

    def _get_reservation_form_token(self):

        return self._get_form_token(self._get_reservation_page())


    def _html_parsing(self, html_page):
        return BeautifulSoup(html_page, 'html.parser')

    def _get_input_fields_from_page(self, html_page):
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

    def _get_reservation_page(self):
        reservation_page_response = requests.post('https://pump-spirit.com/my-pump/public_html/reservar',
                                                  cookies=self.cookies)
        return reservation_page_response

    def is_loggedin(self):

        login_page = self.get_login_page()

        return not ('id="form-register"' in login_page.text)

    def _submit_reservation_form(self, reservation_form_data):

        reservation_page_response = requests.post('https://pump-spirit.com/my-pump/public_html/reservar',
                                            data=reservation_form_data,
                                            cookies=self.cookies)

        return reservation_page_response

    def _get_pump_club_id(self):
        return int(self.config['clubs']['faro'])

    def _get_no_classes_text(self):
        return self.config['general']['no_class_text']

    def _get_classes_from_page (self, html_page):

        parsed_page = self._html_parsing(html_page)
        return parsed_page.findAll("div", {"class": "mypump-class-wrapper"})

    def is_classes_available(self):

        reservation_class_response = self.get_classes_page()

        return not (self._get_no_classes_text() in reservation_class_response.text)

    def get_classes_available(self):

        reservation_class_response = self.get_classes_page()

        if self._get_no_classes_text() in reservation_class_response.text:
            return None

        available_classes_bs4 = self._get_classes_from_page(reservation_class_response.text)

        available_classes_list = []

        for available_class_bs4 in available_classes_bs4:
            available_classes_list.append(PumpClass(available_class_bs4))

        return available_classes_list

    def get_classes_page(self):

        reservation_form_token = self._get_reservation_form_token()

        club_id = self._get_pump_club_id()

        reservation_form = {
            "form[clubsSimple]": club_id,
            "form[_token]": reservation_form_token
        }

        return self._submit_reservation_form(reservation_form)
