from pandas import read_sql, NA, Series, DataFrame
from src.get_date import get_date
from src.get_q import get_q
from src.readSQL import readSQL


def df_insight1(con) -> DataFrame:
    query = readSQL(filename="sql/assessment1.sql")
    df = read_sql(con=con, sql=query)
    df['hiring_date'] = [get_date(st) for st in df['datetime']]
    df['hiring_q'] = [get_q(st) for st in df['datetime']]

    test_year = 2021
    logical = [x.year == test_year if x is not NA else False for x in df['hiring_date']]
    as1 = df.loc[logical]
    as1 = as1.groupby(by=['department', 'job', 'hiring_q'], as_index=False).agg({"id": Series.nunique})
    as1 = as1.pivot_table(
        columns='hiring_q',
        aggfunc=sum,
        index=['department', 'job'],
        fill_value=0)
    as1.reset_index(inplace=True, col_level=1)
    as1.columns = [i2 for _, i2 in as1.columns.values]

    return as1

