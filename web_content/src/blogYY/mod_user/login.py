from flask import render_template
from flask import request
from flask import redirect
from flask import url_for
from flask_login import login_user, login_required
from flask_login.login_manager import LoginManager
from flask_login import logout_user
from web_content import app
from web_content.src.blogYY.mod_user.forms import LoginForm
from web_content.src.blogYY.mod_user.models import User

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
def load_user(user_id):
    return User.get(user_id)


@app.route("/blogYY/login", methods=["GET", "POST"])
def blogYY_page_user_login():
    """
    用户登录页面
    """
    form = LoginForm()
    if form.validate_on_submit():
        username = request.form.get('username', None)
        password = request.form.get('password', None)
        remember_me = request.form.get('remember_me', False)
        user = User(username)
        if user.verify_password(password):
            login_user(user, remember=remember_me)
            return redirect(request.args.get('next') or url_for("blogYY_page_blog_index"))
    return render_template("blogYY/pg_login/login.html", form=form)


@app.route("/logout")
@login_required
def blogYY_page_user_logout():
    logout_user()
    return redirect(url_for("blogYY_page_user_login"))
