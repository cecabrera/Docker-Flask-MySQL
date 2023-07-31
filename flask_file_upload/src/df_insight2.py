from pandas import read_sql, DataFrame
from src.readSQL import readSQL
from sqlalchemy.connectors import Connector


def df_insight2(con: Connector) -> DataFrame:

    query = readSQL(filename="sql/assessment2.sql")

    df = read_sql(con=con, sql=query)

    return df

