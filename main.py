# coding: utf-8
import pump
from time import sleep
import subprocess as s
import sqlite3

from pump_db import PUMPDB


if __name__ == '__main__':

    db_conn = sqlite3.connect('pumpdata.db')

    pump_db_conn = PUMPDB(db_conn)

    pump = pump.Pump()

    while True:

        if not pump.is_loggedin():
            pump.login()

        if (available_classes := pump.get_classes_available()) is not None:
            for available_class in available_classes:

                if pump_db_conn.check_class_notification_last_10_minutes(available_class):
                    pump_db_conn.insert_class(available_class, notified=False)
                else:
                    s.call(['notify-send', available_class.hour + ' ' + available_class.name,
                            available_class.__str__()])
                    pump_db_conn.insert_class(available_class, notified=True)

        sleep(60)
