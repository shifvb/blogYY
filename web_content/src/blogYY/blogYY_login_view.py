from flask import render_template
from web_content import app


@app.route("/login", methods=["GET"])
def login():
    return render_template("blogYY/pg_login/login.html")
