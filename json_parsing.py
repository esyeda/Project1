import sqlalchemy as db
import pandas as pd
import os
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
            connection.commit()

    def pull_list(self, table_name, city):
        query = (f"SELECT * FROM {table_name} "
                 f"WHERE \"address_obj.city\" = '{city}' LIMIT 10;")
        with self.engine.connect() as connection:
            result = connection.execute(db.text(query)).fetchall()
            return result

    def drop(self, table_name):
        command = f"DROP TABLE IF EXISTS {table_name}"
        with self.engine.connect() as connection:
            connection.execute(db.text(command))
