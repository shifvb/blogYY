from datetime import datetime
from flask import render_template
from flask import request
from flask import jsonify
from web_content import app
from web_content.src.blogYY.blogYY_service import search_articles
from web_content.src.blogYY.blogYY_service import add_article
from web_content.src.blogYY.blogYY_service import search_article_by_id
from web_content.src.blogYY.blogYY_service import search_categories
from web_content.src.blogYY.blogYY_service import delete_article_by_id


@app.route("/blogYY/article/", methods=["GET"])
def blogYY_page_article():
    # page limit & offset
    page_size = request.args["page_size"] if hasattr(request.args, "page_size") else 20
    page_num = request.args["page_num"] if hasattr(request.args, "page_num") else 1
    offset = (page_num - 1) * page_size
    # render page
    return render_template("blogYY/index.html", articles=search_articles(limit=page_size, offset=offset))


@app.route("/blogYY/article/<int:article_id>", methods=["GET"])
def blogYY_page_single_article(article_id):
    """
    page for showing single article
    :param article_id: article id
    """
    return render_template("blogYY/index.html", articles=search_article_by_id(article_id))


@app.route("/blogYY/add_article", methods=["GET"])
def blogYY_page_add_article():
    return render_template("blogYY/add_article.html", categories=search_categories())


@app.route("/blogYY/api/v1/add_article", methods=["POST"])
def blogYY_api_add_article_v1():
    """
    api for add article
    url:
        POST /blogYY/api/v1/add_article
    parameter:
        title: article title, str
        author: article author, str
        create_time_str: article create time, YYYY-mm-dd
        content: article content, str
    response:
        {
            "status": "success"
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
        "status": "success"
    })


@app.route("/blogYY/api/v1/del_article/<int:article_id>", methods=["POST"])
def blogYY_api_delete_article_v1(article_id):
    delete_article_by_id(article_id)
    return jsonify({
        "msg": "success"
    })


@app.route("/blogYY/api/v1/mod_article/<int:article_id>", methods=["POST"])
def blogYY_api_modify_article_v1(article_id):
    return jsonify({
        "msg": "开发中，敬请期待！"
    })
