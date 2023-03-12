import sqlite3
import pandas as pd
import numpy as np

class DB():
    def __init__(self, db_name):
        self.db_name = db_name
        try:
            self.connection = sqlite3.connect(self.db_name)
        except Exception as e:
            print(e)

    def get_data(self, query) -> pd.DataFrame: 
        try:
            df = pd.read_sql_query(query, self.connection).drop(['index'], axis = 1)
            return df
        except Exception as e:
            print(e)

    def write_table(self, df, table_name):
        try: 
            df.to_sql(
                name = table_name,
                con = self.connection,
                if_exists = 'replace'
            )
        except Exception as e:
            print(e)