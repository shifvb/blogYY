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
