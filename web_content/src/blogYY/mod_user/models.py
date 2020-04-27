# models.py
import uuid
from flask import g
from flask_login import UserMixin
from werkzeug.security import generate_password_hash
from werkzeug.security import check_password_hash
from flask_login import UserMixin
import json
import uuid

# define profile.json constant, the file is used to
# save user name and password_hash
PROFILE_FILE = "profiles.json"


class User(UserMixin):
    def __init__(self, username):
        self.username = username
        self.id = self.get_id()

    @property
    def password(self):
        return AttributeError("password is not a readable attribute")

    @password.setter
    def password(self, password):
        """
        save user name, id and password hash to json file
        :param password:
        :return:
        """
        self.password_hash = generate_password_hash(password) # todo: remove self
        with open(PROFILE_FILE, 'w+') as f:
            try:
                profiles = json.load(f)
            except ValueError:
                profiles = {}
            profiles[self.username] = [self.password_hash, self.id]
            f.write(json.dumps(profiles))

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
            with open(PROFILE_FILE) as f:
                user_profiles = json.load(f)
                user_info = user_profiles.get(self.username, None)
                if user_info is not None:
                    return user_info[0]
        except IOError:
            return None
        except ValueError:
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
            with open(PROFILE_FILE) as f:
                user_profiles = json.load(f)
                for user_name, profile in user_profiles.items():
                    if profile[1] == user_id:
                        return User(user_name)
        except:
            return None
        return None
