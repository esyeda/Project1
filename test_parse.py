import unittest
import sqlalchemy as db
import json

from json_parsing import Parser

class TestParse(unittest.TestCase):
    
    def setUp(self):
        data = ''
        with open('test_JSON/sampleJSON.txt', 'r') as file:
            data = file.read()
        self.parser = Parser(json.loads(data))
        self.engine = db.create_engine('sqlite:///tripadv.db')
        self.parser.write_to_database("testing")
    
    def test_write_to_database(self):
        # Run to make sure it only keeps unique values
        self.parser.write_to_database("testing")
        with self.engine.connect() as connection:
            result = connection.execute\
                (db.text("SELECT COUNT(*) FROM testing;")).fetchall()
            value = result[0][0]
        self.assertEqual(value, 10)

    def test_pull_list(self):
        db_list = self.parser.pull_list("testing", "Plano")
        self.assertEqual(len(db_list), 9)
        for entry in db_list:
            self.assertIsInstance(entry, db.Row)
    
    def test_drop(self):
        self.assertIn("testing", db.inspect(self.engine).get_table_names())
        query = "DROP TABLE IF EXISTS testing;"
        with self.engine.connect() as connection:
            connection.execute(db.text(query))
            connection.commit()
        self.assertNotIn("testing", db.inspect(self.engine).get_table_names())
