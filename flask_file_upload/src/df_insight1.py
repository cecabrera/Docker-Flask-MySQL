from pandas import read_sql, DataFrame
from src.readSQL import readSQL
from sqlalchemy.connectors import Connector


def df_insight1(con: Connector) -> DataFrame:

    query = readSQL(filename="sql/assessment1.sql")

    df = read_sql(con=con, sql=query)

    # This is not done in the query as the db might change
    df['Quarter'] = [f"Q{q}" for q in df['Quarter']]

    as1 = df.pivot_table(
        columns='Quarter',
        aggfunc=sum,
        values="N",
        index=['department', 'job'],
        fill_value=0)

    as1.reset_index(inplace=True, col_level=1)

    return as1

