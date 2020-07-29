import unittest
from pump import Pump
from bs4 import BeautifulSoup
# class TestPumpClass(unittest.TestCase):
#
#     def test_get_classes(self):
#         pass
#
#
# if __name__ == \'__main__\':
#     unittest.main()

a = '<div class="mypump-class-wrapper"> \
	<div class="mypump-class-hour">07:05</div> \
	<!--<div class="mypump-class-title " onclick="openClassMoreInfo(\'#more-info-1\');" >--> \
	<div class="mypump-class-title"> BODY COMBAT \
		<br> \
			<span>45 min.</span> \
			<!--<span class="mobile"></span>--> \
		</br> \
	</div> \
	<!--<div class="mypump-class-studio desktop "></div>--> \
	<div class="mypump-class-button desktop"> \
		<a href="javascript:void(0);" onclick="reservationMake(\'2e048a27-8544-4543-8f0e-a982597bd425\')"> Reservar </a> \
	</div> \
</div>, \
<div class="mypump-class-wrapper" style="background-color: #fff;"> \
	<div class="mypump-class-hour">19:10</div> \
	<!--<div class="mypump-class-title " onclick="openClassMoreInfo(\'#more-info-2\');" >--> \
	<div class="mypump-class-title"> HIIT \
		<br> \
			<span>30 min.</span> \
			<!--<span class="mobile"></span>--> \
		</br> \
	</div> \
	<!--<div class="mypump-class-studio desktop "></div>--> \
	<div class="mypump-class-button desktop"> \
		<a href="javascript:void(0);" onclick="reservationMake(\'06fae6cb-e2a9-4b92-8e33-e56bb4b23bbb\')"> Reservar </a> \
	</div> \
</div> '

parsed = BeautifulSoup(a, 'html.parser')

classes = parsed.findAll("div", {"class": "mypump-class-wrapper"})

# print(classes)
# print("sadas")
# print(classes[0])
# print(classes[1])
#
# #Get hours
# class_hour = classes[0].find_all("div", {"class": "mypump-class-hour"})[0].text
# print (class_hour)
# #Get Class
# class_info = classes[0].find_all("div", {"class": "mypump-class-title"})[0].text
# class_name, _ , class_duration = class_info.split("\t")
# print (class_name)
# print (class_duration)
#
# reservation_token = classes[0].find_all("div", {"class": "mypump-class-button"})[0].contents[1].attrs['onclick']
#
# print(reservation_token.split('\'')[1])


class PumpClass:

    def __init__(self, pump_class):
        self.parsed_class_data = pump_class
        self.hour = None
        self.name = None
        self.duration = None
        self.reservation_token = None

        self.extract_class_data_from_html()

    def extract_class_data_from_html(self):
        self.extract_hour()
        self.extract_name_and_duration()
        self.extract_reservation_token()

    def extract_hour(self):
        self.hour = self.parsed_class_data.find_all("div", {"class": "mypump-class-hour"})[0].text

    def extract_name_and_duration(self):
        class_info = self.parsed_class_data.find_all("div", {"class": "mypump-class-title"})[0].text
        self.name, _, self.duration = class_info.split("\t")

    def extract_reservation_token(self):
        self.reservation_token = self.parsed_class_data.find_all("div",
                                                                 {"class": "mypump-class-button"}
                                                                 )[0].contents[1].attrs['onclick'].split('\'')[1]

    def __str__(self):
        return self.name + ' ' + self.duration + ' ' + self.hour


for i in classes:
    print(PumpClass(i))
