import sqlite3


def select_db(db_path, query: str):

    con = sqlite3.connect(db_path)

    con.row_factory = sqlite3.Row

    cur = con.cursor()

    cur.execute(query)

    data = cur.fetchall()

    con.close()

    return data