import uuid
from flask import render_template
from web_content import app
from flask_login.login_manager import LoginManager
from flask import request
from flask_login import login_user, login_required
from flask import redirect
from flask_login import logout_user
from flask import url_for
from flask_login import UserMixin
from werkzeug.security import check_password_hash
from web_content.src.blogYY.blogYY_login_service import search_user_by_username
from web_content.src.blogYY.blogYY_login_service import search_user_by_uuid_str

# use login manager to manage session
# 维护用户的会话，关键就在于这个LoginManager对象
# 必须实现load_user callback函数，用于reload user object
# 当密码验证通过后，使用login_user函数来登录用户，
# 这时用户在会话中的状态就是登录状态了
login_manager = LoginManager()
login_manager.session_protection = 'strong'
login_manager.login_view = 'blogYY_page_user_login'
login_manager.init_app(app)


class User(UserMixin):
    def __init__(self, uuid_str: str):
        self.uuid_str = uuid_str
        self.username = search_user_by_uuid_str(uuid_str)['username']

    def get_id(self):
        return self.uuid_str


# 这个callback函数用于reload User object，根据session中存储的user id
@login_manager.user_loader
def user_loader(user_id):
    return User(user_id)


@app.route("/blogYY/login", methods=["GET"])
def blogYY_page_user_login():
    """
    用户登录页面
    """
    return render_template("blogYY/pg_login/login.html")


@app.route("/blogYY/api/v1/login", methods=["POST"])
def blogYY_api_user_login_v1():
    """
    api for user login
    :param username: username, str
    :param password: password, str
    :param remember_me: remember me, str
    :param csrf_token: csrf token
    :return:
        HTTP redirect to:
            request.args.get('next'), if specified 'next' parameter
        or:
            url_for("blogYY_page_log_index"), if not specified 'next' parameter
    """
    username = request.form.get('username', None)
    password = request.form.get('password', None)
    remember_me = request.form.get('remember_me', False)
    _user_info = search_user_by_username(username=username)
    if _user_info and check_password_hash(pwhash=_user_info["password_hash"], password=password):
        login_user(User(_user_info["uuid"]), remember=remember_me)
        return redirect(request.args.get('next') or url_for("blogYY_page_blog_index"))
    else:
        return redirect(url_for("blogYY_page_user_login"))


@app.route("/blogYY/api/v1/logout")
@login_required
def blogYY_page_user_logout():
    """
    api for user logout
    :return:
        HTTP redirect to url_for("blogYY_page_log_index")
    """
    logout_user()
    return redirect(url_for("blogYY_page_blog_index"))
