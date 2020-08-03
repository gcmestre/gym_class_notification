from pump_db import PUMPDB
from pump_class import PumpClass
from bs4 import BeautifulSoup
import sqlite3
import unittest
import os

test_db = "test_db.db"

class TestPumpDB(unittest.TestCase):

    def setUp(self) -> None:

        self.db_conn = sqlite3.connect(test_db)
        self.cursor = self.db_conn.cursor()

        self.pump_db = PUMPDB(self.db_conn)

        self.pump_class = self.create_pump_class()

    def create_pump_class(self):

        with open("../examples/html_class_available.html", "r") as file:
            class_available_html = str(file.readlines())

        parsed_html_class_available = BeautifulSoup(class_available_html, 'html.parser')

        return PumpClass(parsed_html_class_available)


    def test_create_table(self) -> None:

        self.cursor.execute("""SELECT name FROM sqlite_master WHERE type='table' AND name='classes';""")

        self.assertIsNotNone(self.cursor.fetchone())

    def test_insert_class(self) -> None:

        self.pump_db.insert_class(self.pump_class)

        self.cursor.execute("""SELECT name, hour FROM classes WHERE name = '%s' and hour = '%s' """
                                %(self.pump_class.name, self.pump_class.hour))

        inserted_class = self.cursor.fetchone()

        self.assertIsNotNone(inserted_class)
        self.assertEqual(inserted_class[0], self.pump_class.name)
        self.assertEqual(inserted_class[1], self.pump_class.hour)

    def tearDown(self):

        os.remove(test_db)


