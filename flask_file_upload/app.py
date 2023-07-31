# Taken from: https://github.com/sathyainfotech/Excel-File-Upload-SQLite/tree/main

from flask import Flask,render_template,request,flash,redirect,url_for
from os.path import join
import sqlite3
import pandas as pd
from src.readSQL import readSQL
from src.upload_csv import upload_csv
from src.requirements.df_requirement1 import df_requirement1
from src.requirements.df_requirement2 import df_requirement2


app=Flask(__name__)
app.config['UPLOAD_FOLDER']="static\Excel"
app.secret_key="123"

sql_tables_path = [
    "sql\\create\\jobs.sql",
    "sql\\create\\departments.sql",
    "sql\\create\\hired_employees.sql"
]

con=sqlite3.connect("MyData.db")
con.execute("create table if not exists data(pid integer primary key,exceldata TEXT)")
for sql_create_path in sql_tables_path:
    sql = readSQL(filename=sql_create_path)
    con.execute(sql)
con.commit()
con.close()

@app.route("/",methods=['GET','POST'])
def index():

    con = sqlite3.connect("MyData.db")
    con.row_factory = sqlite3.Row
    cur = con.cursor()
    cur.execute("select * from data")
    data = cur.fetchall()
    con.close()

    if request.method == 'POST':
        uploadExcel = request.files['uploadExcel']
        print("Test aqui: ", uploadExcel.filename)
        if uploadExcel.filename != '':

            filepath = join(app.config['UPLOAD_FOLDER'], uploadExcel.filename)
            uploadExcel.save(filepath)

            # Insert the file name into the `data.exceldata` column 
            con = sqlite3.connect("MyData.db")
            cur = con.cursor()
            cur.execute("insert into data(exceldata)values(?)", (uploadExcel.filename,))
            con.commit()
            flash("Excel Sheet Upload Successfully", "success")

            # Create a table with the filename in case it does not exists
            con = sqlite3.connect("MyData.db")
            cur = con.cursor()
            table_name = uploadExcel.filename.replace(".csv", "")

            # Uploads a local file into a table
            upload_csv(con=con, filepath=filepath, table_name=table_name)

            # Loads data table content inside the table
            con = sqlite3.connect("MyData.db")
            con.row_factory = sqlite3.Row
            cur = con.cursor()
            cur.execute("select * from data")
            data = cur.fetchall()
            con.close()

            template = render_template("ExcelUpload.html", data=data)

            return template

    template = render_template(
        template_name_or_list="ExcelUpload.html",
        data=data)

    return template


@app.route('/requirement1')
def requirement1():
    con=sqlite3.connect("MyData.db")
    as1 = df_requirement1(con=con)

    template = render_template(
        template_name_or_list="view_excel.html",
        data=as1.to_html(
            index=False,
            classes="table table-bordered"
        ).replace('<th>','<th style="text-align:center">'))

    return template


@app.route('/requirement2')
def requirement2():
    con=sqlite3.connect("MyData.db")
    as2 = df_requirement2(con=con)

    template = render_template(
        template_name_or_list="view_excel.html",
        data=as2.to_html(
            index=False,
            classes="table table-bordered"
        ).replace('<th>','<th style="text-align:center">'))

    return template


if __name__ == '__main__':
    app.run(debug=True)