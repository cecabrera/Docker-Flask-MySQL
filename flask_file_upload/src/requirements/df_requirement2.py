from pandas import read_sql, DataFrame
from src.readSQL import readSQL
from sqlalchemy.connectors import Connector


def df_requirement2(con: Connector) -> DataFrame:

    query = readSQL(filename="sql/requirement2.sql")

    df = read_sql(con=con, sql=query)

    return df

