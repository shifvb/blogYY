import json
from datetime import datetime
from flask import render_template
from flask import request
from flask import jsonify
from flask import url_for
from flask import abort
from flask_login import current_user
from flask_login import login_required
from web_content import app
from web_content.src.blogYY.blogYY_service import search_articles
from web_content.src.blogYY.blogYY_service import search_articles_info
from web_content.src.blogYY.blogYY_service import search_article_by_id
from web_content.src.blogYY.blogYY_service import count_articles_by_category_id
from web_content.src.blogYY.blogYY_service import group_articles_by_category_id
from web_content.src.blogYY.blogYY_service import add_article
from web_content.src.blogYY.blogYY_service import delete_article_by_id
from web_content.src.blogYY.blogYY_service import update_article_by_id
from web_content.src.blogYY.blogYY_service import search_categories


@app.route("/")
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
        # add category_href attribute
        article["category_href"] = url_for("blogYY_page_article_list", category_id=article["category_id"])
        # restrict the number of content nodes
        _json_obj = json.loads(article["content"])
        _json_obj["ops"] = _json_obj["ops"][:10]
        article["content"] = json.dumps(_json_obj)

    # data processing -> page_control
    article_count = count_articles_by_category_id()
    total_page = article_count // page_size
    if article_count % page_size > 0:
        total_page += 1

    # render page
    return render_template(
        "blogYY/pg_blog_index/bi.html",
        articles=articles,
        total_page=total_page,
        current_user=current_user
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
    article["category_href"] = url_for("blogYY_page_article_list", category_id=article["category_id"])
    # render template
    return render_template("blogYY/pg_single_article/sa.html", article=article, current_user=current_user)


@app.route("/blogYY/add_article", methods=["GET"])
@login_required
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
    # get HTTP get parameters
    category_id = int(request.args["category_id"]) if "category_id" in request.args else None
    page_num = int(request.args["page_num"]) if "page_num" in request.args else 1
    page_size = int(request.args["page_size"]) if "page_size" in request.args else 20
    if page_num <= 0:
        return abort(400)
    if page_size <= 0:
        return abort(400)

    # data processing -> article_counts
    article_counts = group_articles_by_category_id()
    for article_count in article_counts:
        article_count["href"] = url_for("blogYY_page_article_list", category_id=article_count["category_id"])
    article_counts.insert(0, {
        "category_id": None,
        "category_name": "全部博文",
        "article_count": sum([_["article_count"] for _ in article_counts]),
        "href": url_for("blogYY_page_article_list")
    })
    for article_count in article_counts:
        if article_count["category_id"] == category_id:
            this_article_count = article_count

    # data processing -> article_info_list
    offset = (page_num - 1) * page_size
    article_info_list = search_articles_info(limit=page_size, offset=offset, category_id=category_id)
    for article_info in article_info_list:
        article_info["href"] = url_for("blogYY_page_single_article", article_id=article_info["article_id"])

    # data processing -> page control
    article_count = count_articles_by_category_id(category_id)
    total_page = article_count // page_size
    if article_count % page_size > 0:
        total_page += 1

    # render page
    return render_template(
        template_name_or_list="blogYY/pg_article_list/al.html",
        article_counts=article_counts,
        article_info_list=article_info_list,
        this_article_count=this_article_count,
        total_page=total_page,
    )


@app.route("/blogYY/mod_article/<int:article_id>", methods=["GET"])
@login_required
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
@login_required
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
@login_required
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
        "redirect": url_for("blogYY_page_blog_index")
    })


@app.route("/blogYY/api/v1/mod_article/<int:article_id>", methods=["POST"])
@login_required
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
