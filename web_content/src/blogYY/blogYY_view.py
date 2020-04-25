import json
from datetime import datetime
from flask import render_template
from flask import request
from flask import jsonify
from flask import url_for
from flask import abort
from web_content import app
from web_content.src.blogYY.blogYY_service import search_articles
from web_content.src.blogYY.blogYY_service import add_article
from web_content.src.blogYY.blogYY_service import search_article_by_id
from web_content.src.blogYY.blogYY_service import search_categories
from web_content.src.blogYY.blogYY_service import update_article_by_id
from web_content.src.blogYY.blogYY_service import delete_article_by_id
from web_content.src.blogYY.blogYY_service import count_articles


@app.route("/blogYY/blog_index", methods=["GET"])
def blogYY_page_blog_index():
    # page limit & offset
    page_size = int(request.args["page_size"]) if "page_size" in request.args else 5
    page_num = int(request.args["page_num"]) if "page_num" in request.args else 1
    if page_num <= 0:
        return abort(400)
    if page_size <= 0:
        return abort(400)

    # data processing -> articles
    offset = (page_num - 1) * page_size
    articles = search_articles(limit=page_size, offset=offset)
    for article in articles:
        # added href_ful attribute
        article["href_ful"] = url_for("blogYY_page_single_article", article_id=article["id"])
        # restrict the number of content nodes
        _json_obj = json.loads(article["content"])
        _json_obj["ops"] = _json_obj["ops"][:10]
        article["content"] = json.dumps(_json_obj)

    # data processing -> page_control
    article_count = count_articles()
    total_page = article_count // page_size
    if total_page % page_size > 0:
        total_page += 1
    page_link = url_for("blogYY_page_blog_index")

    # render page
    return render_template(
        "blogYY/pg_blog_index/bi.html",
        articles=articles,
        page_link=page_link,
        current_page=page_num,
        total_page=total_page
    )


@app.route("/blogYY/article/<int:article_id>", methods=["GET"])
def blogYY_page_single_article(article_id):
    """
    page for showing single article
    :param article_id: article id
    """
    # data processing
    article = search_article_by_id(article_id)[0]
    article["href_mod"] = url_for("blogYY_page_mod_article", article_id=article["id"])
    article["href_del"] = url_for("blogYY_api_del_article_v1", article_id=article["id"])

    # render template
    return render_template("blogYY/pg_single_article/sa.html", article=article)


@app.route("/blogYY/add_article", methods=["GET"])
def blogYY_page_add_article():
    """
    rendering add article page
    :return: rendered added article page
    """
    return render_template(
        template_name_or_list="blogYY/pg_add_article/aa.html",
        title="",
        content="",
        category_id=1,
        submit_url=url_for('blogYY_api_add_article_v1'),
        redirect_url=url_for('blogYY_page_blog_index'),
        categories=search_categories()
    )


@app.route("/blogYY/article_list", methods=["GET"])
def blogYY_page_article_list():
    """
    rendering article list page
    :return: rendered article list apge
    """
    return render_template("blogYY/pg_article_list/al.html")


@app.route("/blogYY/mod_article/<int:article_id>", methods=["GET"])
def blogYY_page_mod_article(article_id):
    """
    rendering modify article page
    :param article_id: int, article id
    :return: rendered article page
    """
    article = search_article_by_id(article_id)[0]
    return render_template(
        template_name_or_list="blogYY/pg_add_article/aa.html",
        title=article["title"],
        content=article["content"],
        category_id=article["category_id"],
        submit_url=url_for('blogYY_api_mod_article_v1', article_id=article["id"]),
        redirect_url=url_for('blogYY_page_single_article', article_id=article["id"]),
        categories=search_categories()
    )


@app.route("/blogYY/api/v1/add_article", methods=["POST"])
def blogYY_api_add_article_v1():
    """
    api for add article
    url:
        POST /blogYY/api/v1/add_article
    parameter:
        title: article title, str
        create_time_str: article create time, YYYY-mm-dd
        content: article content, str
        category_id: article category id, int
    response:
        {
            "result": "success"
        }
    """
    # timestamp processing
    if request.form["create_time_str"]:
        create_timestamp = int(datetime.strptime(request.form["create_time_str"], "%Y-%m-%d %H:%M:%S").timestamp())
    else:
        create_timestamp = int(datetime.now().timestamp())
    add_article(
        request.form["title"],
        create_timestamp,
        request.form["content"],
        request.form["category_id"]
    )
    return jsonify({
        "result": "success"
    })


@app.route("/blogYY/api/v1/del_article/<int:article_id>", methods=["POST"])
def blogYY_api_del_article_v1(article_id):
    """
    api for delete article
    url:
        POST /blogYY/api/v1/del_article/<int:article_id>
    parameter:
        no HTML form-data parameter
    response:
        {
            "result": "success"
        }
    """
    delete_article_by_id(article_id)
    return jsonify({
        "result": "success",
        "href": url_for("blogYY_page_blog_index")
    })


@app.route("/blogYY/api/v1/mod_article/<int:article_id>", methods=["POST"])
def blogYY_api_mod_article_v1(article_id):
    """
    api for modify article
    url:
        POST /blogYY/api/v1/mod_article/<int:article_id>
    parameter:
        title: article title, str
        content: article content, str
        category_id: article category id, int
    response:
        {
            "result": "success"
        }
    """
    update_article_by_id(
        article_id=article_id,
        title=request.form["title"],
        content=request.form["content"],
        category_id=request.form["category_id"]
    )
    return jsonify({
        "result": "success"
    })
