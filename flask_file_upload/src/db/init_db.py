from src.readSQL import readSQL
import sqlite3


def init_db(
    db_path: str = "MyData.db",
    sql_tables = ["data", "jobs", "departments", "hired_employees"]
) -> None:

    """
    Initialize Database by resetting tables
    """
    
    con = sqlite3.connect(db_path)

    for sql_table in sql_tables:

        con.execute(f"DROP table if exists {sql_table};")

        sql = readSQL(filename=f"sql/create/{sql_table}.sql")

        con.execute(sql)

    con.commit()
