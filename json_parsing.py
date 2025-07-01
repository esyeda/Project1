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
    
    def write_to_database(self, tb_name):
        engine = db.create_engine('sqlite:///tripadv.db')
        self.df.to_sql(tb_name, con=engine, if_exists='append', index=True)

        #removing duplicates, this should work
        with engine.connect() as connection:
            remove_dupes = f"""DELETE FROM {tb_name}
                    WHERE ROWID NOT IN (
                    SELECT MAX(ROWID)
                    FROM {tb_name}
                    GROUP BY Name
                );"""
            connection.execute(db.text(remove_dupes))
            # query_result = 
            # connection.execute(db.text(f"SELECT * FROM {tb_name};")).fetchall()
            # print(pd.DataFrame(query_result))
        self.get_ratings()
    
    def get_ratings(self):
        if type(self.json) != type([]):
            return
        engine = db.create_engine('sqlite:///tripadv.db')
        for location in self.json:
            location_id = location['location_id']
            url = "https://api.content.tripadvisor.com/api/v1/location/search?language=en"
            data = {
                'key': self.key,
                'locationId': location_id
            }
            r = requests.get(url, data=data).json()
            dataFrame = pd.json_normalize(r)
            dataFrame.to_sql("temp", con=engine, if_exists='append', index=True)



        


test = Parser(response)
test.get_ratings()