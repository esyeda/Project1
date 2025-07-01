import json
import sqlalchemy as db
import pandas as pd
import os
import requests

locations = ''
with open('sampleJSON.txt', 'r') as file:
    locations = file.read()
response = json.loads(locations)

class Parser:

    def __init__(self, json):
        if 'data' in json:
            self.json = json['data']
        else:
            self.json = json
        self.df = pd.json_normalize(self.json)
        self.key = os.getenv('TRIPADVISOR_API_KEY')
        self.engine = db.create_engine('sqlite:///tripadv.db')

    def write_to_database(self, tb_name):
        self.df.\
            to_sql(tb_name, con=self.engine, if_exists='append', index=True)

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
        for location in self.json:
            location_id = location['location_id']
            url = """https://api.content.tripadvisor.com/
            api/v1/location/search?language=en"""
            data = {
                'key': self.key,
                'locationId': location_id
            }

            r = requests.get(url, data=data).json()
            dFrame = pd.json_normalize(r)
            dFrame.to_sql\
                ("temp", con=self.engine, if_exists='append', index=True)
        
        join_command = """ CREATE TABLE recommendations AS 
        SELECT * FROM locations 
        JOIN temp ON locations.location_id = temp.location_id;"""
        with self.engine.connect() as connection:
            connection.execute(db.text(join_command))
