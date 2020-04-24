import json
from datetime import datetime
from flask import render_template
from flask import request
from flask import jsonify
from flask import url_for
from web_content import app
from web_content.src.blogYY.blogYY_service import search_articles
from web_content.src.blogYY.blogYY_service import add_article
from web_content.src.blogYY.blogYY_service import search_article_by_id
from web_content.src.blogYY.blogYY_service import search_categories
from web_content.src.blogYY.blogYY_service import update_article_by_id
from web_content.src.blogYY.blogYY_service import delete_article_by_id


@app.route("/blogYY/article/", methods=["GET"])
def blogYY_page_article():
    # page limit & offset
    page_size = request.args["page_size"] if hasattr(request.args, "page_size") else 20
    page_num = request.args["page_num"] if hasattr(request.args, "page_num") else 1
    offset = (page_num - 1) * page_size
    # restrict the number of content nodes
    articles = search_articles(limit=page_size, offset=offset)
    for article in articles:
        _json_obj = json.loads(article["content"])
        _json_obj["ops"] = _json_obj["ops"][:10]
        article["content"] = json.dumps(_json_obj)
    # render page
    return render_template("blogYY/index.html", articles=articles)


@app.route("/blogYY/article/<int:article_id>", methods=["GET"])
def blogYY_page_single_article(article_id):
    """
    page for showing single article
    :param article_id: article id
    """
    return render_template("blogYY/index.html", articles=search_article_by_id(article_id))


@app.route("/blogYY/add_article", methods=["GET"])
def blogYY_page_add_article():
    """
    rendering add article page
    :return: rendered added article page
    """
    return render_template(
        template_name_or_list="blogYY/add_article.html",
        title="",
        content="",
        category_id=1,
        submit_url=url_for('blogYY_api_add_article_v1'),
        categories=search_categories()
    )


@app.route("/blogYY/mod_article/<int:article_id>", methods=["GET"])
def blogYY_page_mod_article(article_id):
    """
    rendering modify article page
    :param article_id: int, article id
    :return: rendered article page
    """
    article = search_article_by_id(article_id)[0]
    return render_template(
        template_name_or_list="blogYY/add_article.html",
        title=article["title"],
        content=article["content"],
        category_id=article["category_id"],
        submit_url=url_for('blogYY_api_mod_article_v1', article_id=article["id"]),
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
def blogYY_api_delete_article_v1(article_id):
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
        "result": "success"
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
