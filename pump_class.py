
class PumpClass:

    def __init__(self, pump_class):
        self.parsed_class_data = pump_class
        self.hour = None
        self.name = None
        self.duration = None
        self.reservation_token = None

        self.extract_class_data_from_html()

    def set_hour(self, new_value):
        self.hour = new_value

    def set_name(self, new_value):
        self.name = new_value

    def set_duration(self, new_value):
        self.duration = new_value

    def set_reservation_token(self, new_value):
        self.reservation_token = new_value

    def extract_class_data_from_html(self):

        self.extract_hour()
        self.extract_name_and_duration()
        self.extract_reservation_token()

    def extract_hour(self):

        self.set_hour(self.parsed_class_data.find_all("div", {"class": "mypump-class-hour"})[0].text)

    def extract_name_and_duration(self):

        class_info = self.parsed_class_data.find_all("div", {"class": "mypump-class-title"})[0].text
        print(class_info)
        #name, _, duration = class_info.split("\t")
        name = class_info
        self.set_name(name)
        self.set_duration(name)

    def extract_reservation_token(self):

        self.set_reservation_token(self.parsed_class_data.find_all("div",
                                                                 {"class": "mypump-class-button"}
                                                                 )[0].contents[1].attrs['onclick'].split('\'')[1])

    def __str__(self):
        return self.name + ' ' + self.duration + ' ' + self.hour
