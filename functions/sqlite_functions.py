from typing import List
from haystack import component
import pandas as pd
pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
pd.set_option('display.width', None)
pd.set_option('display.max_colwidth', None)
import sqlite3
from utils import TEMP_DIR

@component
class SQLiteQuery:

    def __init__(self, sql_database: str):
      self.connection = sqlite3.connect(sql_database, check_same_thread=False)

    @component.output_types(results=List[str], queries=List[str])
    def run(self, queries: List[str], session_hash):
        print("ATTEMPTING TO RUN QUERY")
        dir_path = TEMP_DIR / str(session_hash)
        results = []
        for query in queries:
          result = pd.read_sql(query, self.connection)
          result.to_csv(f'{dir_path}/query.csv', index=False)
          results.append(f"{result}")
        self.connection.close()
        return {"results": results, "queries": queries}
    


def sqlite_query_func(queries: List[str], session_hash):
    dir_path = TEMP_DIR / str(session_hash)
    sql_query = SQLiteQuery(f'{dir_path}/data_source.db')
    try:
      result = sql_query.run(queries, session_hash)
      if len(result["results"][0]) > 500:
        print("QUERY TOO LARGE")
        return {"reply": "query result too large to be processed by llm, the query results are in our query.csv file"}
      else:   
        return {"reply": result["results"][0]}

    except Exception as e:
      reply = f"""There was an error running the SQL Query = {queries}
              The error is {e},
              You should probably try again.
              """
      return {"reply": reply}
