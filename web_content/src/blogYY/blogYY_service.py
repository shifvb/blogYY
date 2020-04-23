from datetime import datetime
from flask import g
from flask import url_for


def search_articles(limit: int, offset: int):
    """
    return articles
    """
    _cursor = g.blogYY_conn.cursor()
    _cursor.execute("""
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
    LIMIT ? 
    OFFSET ?;""", (limit, offset))
    return [{
        "id": _[0],
        "title": _[1],
        "create_time_str": datetime.fromtimestamp(_[2]).strftime("%Y-%m-%d %H:%M:%S"),
        "content": _[3][:499] + "..." if len(_[3]) > 512 else _[3],
        "category": _[4],
        "href_ful": url_for("blogYY_page_single_article", article_id=_[0])
    } for _ in _cursor.fetchall()]


def search_article_by_id(article_id: int):
    """
    search single article by article id
    :return: dict contains article information
    """
    _cursor = g.blogYY_conn.cursor()
    _cursor.execute("""
        SELECT
            `id`,  
            `title`,
            `create_timestamp`,
            `content`,
            `category_id`
        FROM 
            `article` 
        WHERE
            `id`=?;
        """, (article_id,))
    return [{
        "id": _[0],
        "title": _[1],
        "create_time_str": datetime.fromtimestamp(_[2]).strftime("%Y-%m-%d %H:%M:%S"),
        "content": _[3],
        "category": _[4],
        "href_mod": url_for("blogYY_api_modify_article_v1", article_id=_[0]),
        "href_del": url_for("blogYY_api_delete_article_v1", article_id=_[0])
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
