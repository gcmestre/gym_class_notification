import requests
import configparser
from bs4 import BeautifulSoup

input_form_url = 'https://pump-spirit.com/my-pump/public_html/login'

config = configparser.ConfigParser()
config.read('config.cfg')

login_data = {
    "username": config['credentials']["username"],
    "password": config['credentials']["password"]
}

no_class_available_text = "Não há aulas disponíveis para marcação."

club_id = {"faro": 87}

cookies = None

#r = requests.post('https://pump-spirit.com/my-pump/public_html/login', 
#            data={"username":"goncalo2120@gmail.com",
#                  "password":"microfone",
#                  "_token":"Kc0_4PHxVXSn6flM6SQjYxxBkJSdI_uouwv8ON_1m3w"})
#r = requests.get('https://pump-spirit.com/my-pump/public_html/reservar', auth=('user', 'pass'))


# form[username]: goncalo2120@gmail.com
# form[password]: microfone
# form[_token]: Kc0_4PHxVXSn6flM6SQjYxxBkJSdI_uouwv8ON_1m3w


def is_class_available(html):
    return no_class_available_text in html

def is_logged_in(html):
    return not ('id="form-register"' in html)

def html_parsing (login_page):
    
    return BeautifulSoup(login_page, 'html.parser')

def get_input_fields_from_page (html_page):
    
    return html_page.find_all('input')

def get_classes_from_page (html_page):
    
    return html_page.findAll("div", {"class": "mypump-class-wrapper"})

def get_login_page():
    login_page_response = requests.post('https://pump-spirit.com/my-pump/public_html/login')

    global cookies
    cookies = login_page_response.cookies

    return login_page_response

def get_reservation_page():
    reservation_page_response = requests.post('https://pump-spirit.com/my-pump/public_html/reservar', cookies=cookies)
    return reservation_page_response

def generate_login_dict():
    
    login_page = get_login_page()

    parsed_login_page = html_parsing(login_page.text)
    
    login_input_fields = get_input_fields_from_page(parsed_login_page)

    login_form = {
        "form[username]":login_data['username'],
        "form[password]":login_data['password'],
        "form[_token]":login_input_fields[-1]['value']
    }

    return login_form

    
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


reservation_form_data = generate_reservation_dict()
club_revervation_status_response = submit_reservation_form(reservation_form_data)

# with open("club_revervation_status_response.html","w") as file:
#    file.write(reservation_submit_response.text)

#with open ("club_revervation_status_response.html", "r") as file:
#    club_revervation_status_response =  file.read()

#class_status = html_parsing(reservation_submit_response)

class_status = html_parsing(club_revervation_status_response.text)


available_classes = get_classes_from_page(class_status)

print("Is there any class available? - ", is_class_available(class_status))
