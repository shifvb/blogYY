from datetime import datetime
import sqlite3


def _create(cursor):
    cursor.execute("""
        CREATE TABLE `user` (
            `uuid` TEXT PRIMARY KEY NOT NULL,
            `username` TEXT NOT NULL,
            `password_hash` TEXT NOT NULL
        );
    """)


def _insert(conn, cursor, uuid: str, username: str, password_hash: str):
    cursor.execute("""
        INSERT INTO `user` (
            `uuid`,
            `username`,
            `password_hash`
        ) VALUES (
            ?, ?, ?
        );
    """, (
        uuid,
        username,
        password_hash
    ))
    conn.commit()


def _select(cursor):
    cursor.execute("""
        SELECT
            `uuid`,
            `username`,
            `password_hash`
        FROM
            `user` 
    ;""")
    print("-" * 10, end=' ')
    print("TABLE `user`", end=' ')
    print("-" * 10)
    for row in cursor.fetchall():
        print(row)
    print()


def immigrant_user(is_create=False, is_insert=False, is_select=True):
    conn = sqlite3.connect("blogYY.db")
    cursor = conn.cursor()
    if is_create is True:
        _create(cursor)
    if is_insert is True:
        _insert(
            conn,
            cursor,
            "b38b5f26-6c30-4ef7-8495-d55c63eca781",
            "woshiduxingxiayu",
            "pbkdf2:sha256:150000$rwXhzkCl$fc0238b19b78452969034780cc185266e7335ec9261bc1c0b9caa335423f3d5e"
        )
    if is_select is True:
        _select(cursor)
