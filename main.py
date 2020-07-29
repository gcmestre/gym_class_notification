# coding: utf-8
import pump
from time import sleep
import subprocess as s


if __name__ == '__main__':

    pump = pump.Pump()

    while True:

        if not pump.is_loggedin():
            print ("is not logged in")
            pump.login()

        if (available_classes := pump.get_classes_available()) is not None:
            for available_class in available_classes:
                s.call(['notify-send', available_class.hour + ' ' + available_class.name, available_class.__str__()])

        print("Sleeping")
        sleep(60)

