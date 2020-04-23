import sqlite3
from flask import g, Flask

# general config
app = Flask(__name__)
with open("secret_key", 'rb') as f:
    app.secret_key = f.read()

# import views
import web_content.src.blogYY.blogYY_view


# establish database connection
@app.before_request
def before_request():
    g.blogYY_conn = sqlite3.connect("../database/blogYY/blogYY.db")


# close database connection
@app.teardown_request
def teardown_request(rsp):
    try:
        g.blogYY_conn.close()
    except sqlite3.Error:
        pass
