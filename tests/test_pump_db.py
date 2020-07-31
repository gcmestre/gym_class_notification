from pump_db import PUMPDB
from pump_class import PumpClass
import sqlite3
import unittest
import os

test_db = "test_db.db"

class TestPumpDB(unittest.TestCase):

    def setUp(self) -> None:

        self.db_conn = sqlite3.connect(test_db)
        self.cursor = self.db_conn.cursor()

    def test_create_table(self) -> None:

        PUMPDB(self.db_conn)

        self.cursor.execute("""SELECT name FROM sqlite_master WHERE type='table' AND name='classes';""")

        self.assertIsNotNone(self.cursor.fetchone())

    def test_insert_class(self) -> None:

        pumpdb =  PUMPDB(self.db_conn)

        pumpclass = PumpClass()

        pumpclass.set_hour("10:10")
        pumpclass.set_name("Test class 1")

        pumpdb.insert_class(pumpclass)

        #self.cursor.execute("""SELECT name FROM sqlite_master WHERE type='table' AND name='classes';""")

        self.assertIsNotNone(None)

    def tearDown(self):

        os.remove(test_db)


