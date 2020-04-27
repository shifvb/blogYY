import os
import sqlite3
from flask import g, Flask
from flask_wtf.csrf import CSRFProtect

# general config
app = Flask(__name__)
app.secret_key = os.urandom(64)

# import views
import web_content.src.blogYY.blogYY_view
import web_content.src.blogYY.blogYY_login_view

# csrf protect
CSRFProtect().init_app(app)


# establish database connection
@app.before_request
def before_request():
    g.blogYY_conn = sqlite3.connect("../database/blogYY/blogYY.db")


# close database connection
@app.teardown_request
def teardown_request(rsp):
    try:
        g.blogYY_conn.close()
    except sqlite3.Error as e:
        print("sqlite3 Error: " + str(e))
    except Exception as e:
        print(str(e))
