from datetime import datetime
import time
import sqlite3



def adapt_datetime(ts):
    return time.mktime(ts.timetuple())


sqlite3.register_adapter(datetime, adapt_datetime)


class PUMPDB:

    def __init__(self, conn):

        self.conn = conn

        self.cursor = self.conn.cursor()

        self.create_table_if_not_exists()

    def create_table_if_not_exists(self):

        query = """
                    CREATE TABLE IF NOT EXISTS classes (
                        timestamp DATETIME , 
                        name TEXT, 
                        hour TEXT,
                        notified BOOL) 
        """

        self.execute_query(query)


    def execute_query(self, query):

        try:
            return self.cursor.execute(query)
        except Exception as e:
            print("Error inserting query %s" % query)
            print("Exception %s" % e)

    def fetch_all(self):

        return self.cursor.fetchall()

    def fetch_one(self):

        return self.cursor.fetchone()


    def commit(self):

        self.conn.commit()

    def close(self):

        self.conn.close()
        self.conn.close()

    def fetch_all_classes(self):

        query = """SELECT * FROM CLASSES"""

        self.execute_query(query)

        return self.fetchall()

    def insert_class(self, pump_class, notified=False):


        query = """INSERT INTO CLASSES ('timestamp' , 'name', 'hour', 'notified') VALUES (
                            Datetime('now'),'%s', '%s', %s)""" % (pump_class.name, pump_class.hour, notified)

        self.execute_query(query)

        return self.commit()

    def check_class_notification_last_10_minutes(self, pump_class):
        """
            Verify is was send a notification for this class in the past 5 minutes
        :param pump_class:
        :return:
        """

        query = """select * from classes where 
                        timestamp > Datetime('now','-10 minutes') and 
                        name = '%s' and 
                        notified = True""" %(pump_class.name)

        self.execute_query(query)

        return self.fetch_one()


