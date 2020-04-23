import sqlite3


def _create_table(cursor):
    cursor.execute("""
        CREATE TABLE `category` (
            `id` INTEGER PRIMARY KEY NOT NULL,
            `name` TEXT NOT NULL
        );""")


def _insert(conn, cursor, name: str):
    cursor.execute("""
        INSERT INTO `category` (
            `name`
        ) VALUES (
            ?
        );
        """, (name,))
    conn.commit()


def _select(cursor):
    cursor.execute("""
        SELECT
            `id`,
            `name`
        FROM
            `category` 
        ;
    """)
    print("-" * 10, end=' ')
    print("TABLE `category`", end=' ')
    print("-" * 10)
    for row in cursor.fetchall():
        print(row)
    print()


def immigrant_category(is_create=False, is_insert=False, is_select=True):
    conn = sqlite3.connect("blogYY.db")
    cursor = conn.cursor()
    if is_create is True:
        _create_table(cursor)
    if is_insert is True:
        _insert(conn, cursor, "原创")
        _insert(conn, cursor, "股票")
        _insert(conn, cursor, "期货")
        _insert(conn, cursor, "宏观经济")
        _insert(conn, cursor, "产业研究")
        _insert(conn, cursor, "企业研究")
        _insert(conn, cursor, "人生")
        _insert(conn, cursor, "日记")
        _insert(conn, cursor, "杂谈")
        _insert(conn, cursor, "财富")
        _insert(conn, cursor, "艺术")
        _insert(conn, cursor, "旅游")
        _insert(conn, cursor, "影评")
        _insert(conn, cursor, "电影")
        _insert(conn, cursor, "看世界")
        _insert(conn, cursor, "私密博文")
    if is_select is True:
        _select(cursor)


if __name__ == '__main__':
    immigrant_category()
