import json
import sqlalchemy as db
import pandas as pd
import os
import requests
from dotenv import load_dotenv


class Parser:

    def __init__(self, json):
        load_dotenv()
        if 'data' in json:
            self.json = json['data']
        else:
            self.json = json
        self.df = pd.json_normalize(self.json)
        self.key = os.getenv('TRIPADVISOR_API_KEY')
        self.engine = db.create_engine('sqlite:///tripadv.db')

    def write_to_database(self, tb_name):
        self.df.\
            to_sql(tb_name, con=self.engine, if_exists='append', index=False)

        # removing duplicates, this should work
        with self.engine.connect() as connection:
            remove_dupes = f"""DELETE FROM {tb_name}
                    WHERE ROWID NOT IN (
                    SELECT MAX(ROWID)
                    FROM {tb_name}
                    GROUP BY Name
                );"""
            connection.execute(db.text(remove_dupes))
            # query_result =
            # connection.execute
            # (db.text(f"SELECT * FROM {tb_name};")).fetchall()
            # print(pd.DataFrame(query_result))
        self.get_ratings()

    def get_ratings(self):
        if not isinstance(self.json, type([])):
            return
        rows = []
        for location in self.json:
            location_id = int(location['location_id'])
            url = (f"https://api.content.tripadvisor.com/api/v1/location/"
            f"{location_id}/details")
            headers = {"accept": "application/json"}
            data = {
                'key': self.key
            }

            r = requests.get(url, headers=headers, params=data)
            if r.status_code == 200:
                flattened = pd.json_normalize(r.json())
                print(flattened)
                rows.append(flattened)
        df = pd.concat(rows, ignore_index=True)
        df = df.infer_objects()
        print(df)
        print(df.dtypes)
        # df.to_sql("temp", con=self.engine, if_exists='append', index=False)

        join_command = """CREATE TABLE recommendations AS
         SELECT * FROM locations
         JOIN temp ON locations.location_id = temp.location_id;"""
        with self.engine.connect() as connection:
            connection.execute(db.text(join_command))

with open('sampleJSON.txt', 'r') as file:
    location = file.read()
test = Parser(json.loads(location))
test.write_to_database("locations")
