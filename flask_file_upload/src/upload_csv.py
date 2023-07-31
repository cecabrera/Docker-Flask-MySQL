from pandas import read_csv, read_sql
import sqlite3


def upload_csv(db_path, filepath, table_name):

    con = sqlite3.connect(db_path)

    # Read the CSV as a DataFrame
    df = read_csv(
        filepath_or_buffer=filepath,
        header=None)

    # Get Column Names
    df.columns = read_sql(
        con=con,
        sql=f"SELECT * FROM {table_name} LIMIT 0"
    ).columns

    # Upload the CSV data into the table
    df.to_sql(
        con=con,
        if_exists="append",
        name=table_name,
        index=False,
        method="multi")

    n = read_sql(
        con=con,
        sql=f"SELECT COUNT(*) AS n FROM {table_name}"
    ).values[0][0]

    print(f"{df.shape[0]} rows added into `{table_name}` table. Nrows: {n}")
