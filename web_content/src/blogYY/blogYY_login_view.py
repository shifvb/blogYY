from flask import render_template
from web_content import app
from flask_login.login_manager import LoginManager
from flask import request
from flask_login import login_user, login_required
from flask import redirect
from flask_login import logout_user
from flask import url_for

# use login manager to manage session
# 维护用户的会话，关键就在于这个LoginManager对象
# 必须实现load_user callback函数，用于reload user object
# 当密码验证通过后，使用login_user函数来登录用户，
# 这时用户在会话中的状态就是登录状态了
login_manager = LoginManager()
login_manager.session_protection = 'strong'
login_manager.login_view = 'blogYY_page_user_login'
login_manager.init_app(app=app)


# 这个callback函数用于reload User object，根据session中存储的user id
@login_manager.user_loader
def user_loader(user_id):
    return User.get(user_id)


@app.route("/blogYY/login", methods=["GET", "POST"])
def blogYY_page_user_login():
    """
    用户登录页面
    """
    if request.method == "POST":
        username = request.form.get('username', None)
        password = request.form.get('password', None)
        remember_me = request.form.get('remember_me', False)
        user = User(username)
        if user.verify_password(password):
            login_user(user, remember=remember_me)
            return redirect(request.args.get('next') or url_for("blogYY_page_blog_index"))
    return render_template("blogYY/pg_login/login.html")


@app.route("/logout")
@login_required
def blogYY_page_user_logout():
    logout_user()
    return redirect(url_for("blogYY_page_user_login"))


# models.py
import uuid
from flask import g
from flask_login import UserMixin
from werkzeug.security import generate_password_hash
from werkzeug.security import check_password_hash


class User(UserMixin):
    def __init__(self, username):
        self.username = username
        self.id = self.get_id()

    def verify_password(self, password):
        password_hash = self.get_password_hash()
        if password_hash is None:
            return False
        return check_password_hash(password_hash, password)

    def get_password_hash(self):
        """
        try to get password hash form file.

        :return password_hash:
            if there is corresponding user in the file, return
            password hash. If there is no corresponding user,
            return None.
        """
        try:
            _cursor = g.blogYY_conn.cursor()
            _cursor.execute("""SELECT `password_hash` FROM `user` WHERE `username`=?;""", (self.username,))
            _user_info_tuple = _cursor.fetchone()
            if _user_info_tuple is not None:
                return _user_info_tuple[0]
        except IOError:
            return None
        except ValueError:
            return None
        return None

    def get_id(self):
        """
        get user id from profile file. If not exist, it will generate a
        uuid for the user.
        :return:
        """
        if self.username is None:
            return str(uuid.uuid4())

        _cursor = g.blogYY_conn.cursor()
        _cursor.execute("""SELECT `uuid` FROM `user` WHERE `username`=?;""", (self.username,))
        _user_info_tuple = _cursor.fetchone()

        if _user_info_tuple is not None:
            return _user_info_tuple[0]
        else:
            return str(uuid.uuid4())

    @staticmethod
    def get(user_id):
        """
        try to return user_id corresponding user object.
        This method is used by load_user callback function
        :param user_id:
        :return:
        """
        if not user_id:
            return None
        try:
            _cursor = g.blogYY_conn.cursor()
            _cursor.execute("""SELECT `username` FROM `user` WHERE `uuid`=?;""", (user_id,))
            _user_info_tuple = _cursor.fetchone()
            if _user_info_tuple is not None:
                return User(_user_info_tuple[0])
        except:
            return None
        return None
