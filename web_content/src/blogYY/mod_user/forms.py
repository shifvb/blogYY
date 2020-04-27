# forms.py
from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField, PasswordField
from wtforms.validators import DataRequired


# 定义的表单都需要继承自FlaskForm
class LoginForm(FlaskForm):
    # 域初始化时，第一个参数用于设置label属性
    username = StringField("User Name", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    remember_me = BooleanField("remember me", default=False)
