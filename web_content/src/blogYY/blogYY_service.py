from datetime import datetime
from flask import g


def search_articles(limit: int, offset: int):
    """
    return articles
    """
    _cursor = g.blogYY_conn.cursor()
    _cursor.execute("""
    SELECT
        `article`.`id`,  
        `article`.`title`,
        `article`.`create_timestamp`,
        `article`.`content`,
        `category`.`id`,
        `category`.`name`
    FROM 
        `article` 
    INNER JOIN
        `category`
    ON
        `article`.`category_id` = `category`.`id`
    ORDER BY 
        `create_timestamp` DESC 
    LIMIT ? 
    OFFSET ?;""", (limit, offset))
    return [{
        "id": _[0],
        "title": _[1],
        "create_time_str": datetime.fromtimestamp(_[2]).strftime("%Y-%m-%d %H:%M:%S"),
        "content": _[3],
        "category_id": _[4],
        "category_name": _[5],
    } for _ in _cursor.fetchall()]


def search_articles_info(limit: int, offset: int, category_id=None):
    """
    return info of articles
    """
    _cursor = g.blogYY_conn.cursor()
    if category_id is None:
        _cursor.execute("""
            SELECT
                `article`.`id`,  
                `article`.`title`,
                `article`.`create_timestamp`
            FROM 
                `article` 
            ORDER BY 
                `create_timestamp` DESC 
            LIMIT ? 
            OFFSET ?;
            """, (limit, offset))
    else:
        _cursor.execute("""
            SELECT
                `id`,  
                `title`,
                `create_timestamp`
            FROM 
                `article` 
            WHERE
                `category_id`=?
            ORDER BY 
                `create_timestamp` DESC 
            LIMIT ? 
            OFFSET ?;""", (category_id, limit, offset))
    return [{
        "article_id": _[0],
        "article_title": _[1],
        "create_time_str": datetime.fromtimestamp(_[2]).strftime("%Y-%m-%d %H:%M:%S"),
    } for _ in _cursor.fetchall()]


def search_article_by_id(article_id: int):
    """
    search single article by article id
    :return: dict contains article information
    """
    _cursor = g.blogYY_conn.cursor()
    _cursor.execute("""
        SELECT
            `article`.`id`,  
            `article`.`title`,
            `article`.`create_timestamp`,
            `article`.`content`,
            `article`.`category_id`,
            `category`.`name`
        FROM 
            `article`
        INNER JOIN
            `category`
        ON
            `article`.`category_id` = `category`.`id`
        WHERE
            `article`.`id`=?;
        """, (article_id,))
    return [{
        "id": _[0],
        "title": _[1],
        "create_time_str": datetime.fromtimestamp(_[2]).strftime("%Y-%m-%d %H:%M:%S"),
        "content": _[3],
        "category_id": _[4],
        "category_name": _[5]
    } for _ in [_cursor.fetchone()]]


def add_article(title, create_timestamp, content, category_id):
    """
    add an article
    """
    _cursor = g.blogYY_conn.cursor()
    _cursor.execute("""
        INSERT INTO `article` ( 
            `title`,
            `create_timestamp`,
            `content`,
            `category_id`
        ) VALUES (
            ?, ?, ?, ?
        );
        """, (
        title, create_timestamp, content, category_id
    ))
    g.blogYY_conn.commit()


def search_categories():
    """
    return categories
    """
    _cursor = g.blogYY_conn.cursor()
    _cursor.execute("""
        SELECT
            `id`,
            `name`
        FROM 
            `category` 
        ;
    """)
    return [{
        "id": _[0],
        "name": _[1],
    } for _ in _cursor.fetchall()]


def delete_article_by_id(article_id: int):
    """
    delete a particular article by its id
    """
    _cursor = g.blogYY_conn.cursor()
    _cursor.execute("""
        DELETE FROM
            `article`
        WHERE
            `id` = ?
        ;
    """, (article_id,))
    g.blogYY_conn.commit()


def update_article_by_id(article_id: int, title: str, content: str, category_id: int):
    """
    update article data by its id
    :param article_id: article id
    :param title: article title
    :param content: article content
    :param category_id: category id
    """
    _cursor = g.blogYY_conn.cursor()
    _cursor.execute("""
    UPDATE
        `article`
    SET
        `title` = ?,
        `content` = ?,
        `category_id` = ?
    WHERE
        `id` = ?
    ;
    """, (title, content, category_id, article_id))
    g.blogYY_conn.commit()


def count_articles_by_category_id(category_id=None):
    """
    count articles
    :param category_id: int, can be set to None if not specify category
    """
    _cursor = g.blogYY_conn.cursor()
    if category_id is None:
        _cursor.execute("""
            SELECT
                COUNT (*)
            FROM
                `article`
            ;
        """)
    else:
        _cursor.execute("""
            SELECT
                COUNT (*)
            FROM
                `article`
            WHERE
                `category_id`=?
            ;
        """, (category_id,))
    return _cursor.fetchone()[0]


def group_articles_by_category_id():
    """
    search the count of each category
    :return:
    """
    _cursor = g.blogYY_conn.cursor()
    _cursor.execute("""
        SELECT
            `category`.`id`,
            `category`.`name`,
            COUNT(`article`.`id`)
        FROM
            `article` INNER JOIN `category`
        ON
            `article`.`category_id` = `category`.`id`
        GROUP BY
            `category`.`id`
        ;
        """)
    return [{
        "category_id": _[0],
        "category_name": _[1],
        "article_count": _[2]
    } for _ in _cursor.fetchall()]
