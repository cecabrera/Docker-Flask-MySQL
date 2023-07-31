# Taken from: https://github.com/sathyainfotech/Excel-File-Upload-SQLite/tree/main

from flask import Flask, render_template, request, flash, redirect, url_for
from os.path import join
import sqlite3
from pandas import read_csv, read_sql
from src.upload_csv import upload_csv
from src.db.init_db import init_db
from src.db.select_db import select_db
from src.requirements.df_requirement1 import df_requirement1
from src.requirements.df_requirement2 import df_requirement2


app=Flask(__name__)
app.config['UPLOAD_FOLDER']="static\Excel"
app.secret_key="123"
db_path = "MyData.db"

# Initialize Database by resetting tables
init_db(
    db_path=db_path,
    sql_tables=["data", "jobs", "departments", "hired_employees"])

@app.route("/",methods=['GET','POST'])
def index():

    data = select_db(db_path=db_path, query="select * from data")

    if request.method == 'POST':
        uploadExcel = request.files['uploadExcel']
        if uploadExcel.filename != '':

            filepath = join(app.config['UPLOAD_FOLDER'], uploadExcel.filename)
            uploadExcel.save(filepath)

            # Insert the file name into the `data.exceldata` column 
            con = sqlite3.connect(db_path)
            cur = con.cursor()
            cur.execute("insert into data(exceldata)values(?)", (uploadExcel.filename,))
            con.commit()
            flash("Excel Sheet Upload Successfully", "success")

            # Create a table with the filename in case it does not exists
            table_name = uploadExcel.filename.replace(".csv", "")

            # Uploads a local file into a table
            upload_csv(db_path=db_path, filepath=filepath, table_name=table_name)

            # Loads data table content inside the table
            data = select_db(db_path=db_path, query="select * from data")

            template = render_template("ExcelUpload.html", data=data)

            return template

    template = render_template(
        template_name_or_list="ExcelUpload.html",
        data=data)

    return template


@app.route('/view_excel/<string:id>')
def view_excel(id):

    data = select_db(db_path=db_path, query=f"select * from data where pid={id}")

    for val in data:

        path = join("static/Excel/",val[1])

        print(val[1])

        data = read_csv(filepath_or_buffer=path, header=None)

    template = render_template(
        template_name_or_list="view_excel.html",
        data=data.to_html(
            index=False,
            classes="table table-bordered"
        ).replace('<th>','<th style="text-align:center">'))

    return template

@app.route('/delete_record/<string:id>')
def delete_record(id):
    try:
        con=sqlite3.connect("MyData.db")
        cur=con.cursor()
        cur.execute("delete from data where pid=?",[id])
        con.commit()
        flash("CSV Deleted Successfully Locally. It is still in Database","success")
        con.close()
    except:
        flash("Record Deleted Failed", "danger")
    finally:
        return redirect(url_for("index"))


@app.route('/jobs')
def jobs():

    con=sqlite3.connect("MyData.db")
    jobs_df = read_sql(con=con, sql="SELECT * FROM jobs")
    
    template = render_template(
        template_name_or_list="view_excel.html",
        data=jobs_df.to_html(
            index=False,
            classes="table table-bordered"
        ).replace('<th>','<th style="text-align:center">'))

    return template

@app.route('/requirement1')
def requirement1():

    con=sqlite3.connect(db_path)

    as1 = df_requirement1(con=con)

    template = render_template(
        template_name_or_list="requirement1.html",
        data=as1.to_html(
            index=False,
            classes="table table-bordered"
        ).replace('<th>','<th style="text-align:center">'))

    return template


@app.route('/requirement2')
def requirement2():
    con=sqlite3.connect(db_path)
    as2 = df_requirement2(con=con)

    template = render_template(
        template_name_or_list="requirement2.html",
        data=as2.to_html(
            index=False,
            classes="table table-bordered"
        ).replace('<th>', '<th style="text-align:center">'))

    return template


if __name__ == '__main__':
    app.run(debug=True)