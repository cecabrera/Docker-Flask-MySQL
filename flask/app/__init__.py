from flask import Flask

app = Flask(__name__)
app.config['UPLOAD_FOLDER']="static\csv"

from app import views
