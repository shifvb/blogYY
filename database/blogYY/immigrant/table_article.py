from datetime import datetime
import sqlite3


def _create(cursor):
    cursor.execute("""
        CREATE TABLE `article` (
            `id` INTEGER PRIMARY KEY NOT NULL,
            `title` TEXT NOT NULL,
            `create_timestamp` INTEGER NOT NULL,
            `content` TEXT NOT NULL,
            `category_id` INTEGER NOT NULL
        );
    """)


def _insert(conn, cursor, title: str, create_time_str: str, content: str, category_id: int):
    cursor.execute("""
        INSERT INTO `article` (
            `title`,
            `create_timestamp`,
            `content`,
            `category_id`
        ) VALUES (
            ?, ?, ?, ?
        );
    """, (
        title,
        datetime.strptime(create_time_str, "%Y-%m-%d %H:%M:%S").timestamp(),
        content,
        category_id
    ))
    conn.commit()


def _select(cursor):
    cursor.execute("""
        SELECT
            `id`,
            `title`,
            `create_timestamp`,
            `content`,
            `category_id`
        FROM
            `article` 
        ORDER BY 
            `create_timestamp` DESC
    ;""")
    print("-" * 10, end=' ')
    print("TABLE `article`", end=' ')
    print("-" * 10)
    for row in cursor.fetchall():
        print(row)
    print()


def immigrant_article(is_create=False, is_insert=False, is_select=True):
    conn = sqlite3.connect("blogYY.db")
    cursor = conn.cursor()
    if is_create is True:
        _create(cursor)
    if is_insert is True:
        _insert(conn, cursor, "title", "2020-04-22 14:57:14", "content", 1)
    if is_select is True:
        _select(cursor)


if __name__ == '__main__':
    immigrant_article()
