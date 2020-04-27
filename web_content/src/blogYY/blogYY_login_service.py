from flask import g


def search_user_by_username(username: str):
    """
    search user by username
    :param username: username, str
    :return:
        Only return one single user information, which is not working
        properly when database contains 2 users with the exactly same
        username.

        if cannot search username in database:
            None

        or:
        {
            "uuid": [user uuid, str],
            "password_hash": [user password_hash, str],
        }
    """
    _cursor = g.blogYY_conn.cursor()
    _cursor.execute("""
        SELECT
            `uuid`,
            `password_hash`
        FROM
            `user`
        WHERE
            `username`=?
        ;
    """, (username,))
    _db_rsp = _cursor.fetchone()
    if _db_rsp is None:
        return None
    return {
        "uuid": _db_rsp[0],
        "password_hash": _db_rsp[1]
    }


def search_user_by_uuid_str(uuid_str: str):
    """
    search user information by its uuid str
    :param uuid_str: uuid str
    :return:
        {
            "username": [username, str],
            "password_hash": [user password_hash, str],
        }
    """
    _cursor = g.blogYY_conn.cursor()
    _cursor.execute("""
        SELECT
            `username`,
            `password_hash`
        FROM 
            `user`
        WHERE
            `uuid`=?
        ;
    """, (uuid_str,))
    _db_rsp = _cursor.fetchone()
    if _db_rsp is None:
        return None
    return {
        "username": _db_rsp[0],
        "password_hash": _db_rsp[1],
    }
