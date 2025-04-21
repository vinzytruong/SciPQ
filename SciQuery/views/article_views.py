from flask import Blueprint, request
from models import ArticleModel
from utils.response import success_response, error_response

article_bp = Blueprint("article", __name__)

@article_bp.route("/articles", methods=["POST"])
def create_article():
    data = request.get_json()
    required_fields = ["title", "content", "publication_date", "author_id", "field_id"]
    if not data or not all(field in data for field in required_fields):
        return error_response("Missing required fields", 400)
    
    model = ArticleModel()
    result = model.create_article(
        data["title"],
        data["content"],
        data["publication_date"],
        data["author_id"],
        data["field_id"]
    )
    if result:
        article = result["p"]
        author = result["a"]
        field = result["f"]
        return success_response(
            data={
                "id": article["id"],
                "title": article["title"],
                "content": article["content"],
                "publication_date": article["publication_date"],
                "author": {"id": author["id"], "name": author["name"]},
                "field": {"id": field["id"], "name": field["name"]}
            },
            message="Article created successfully"
        ), 201
    return error_response("Failed to create article", 500)

@article_bp.route("/articles", methods=["GET"])
def get_all_articles():
    model = ArticleModel()
    results = model.get_all_articles()
    articles = []
    for result in results:
        article = result["p"]
        author = result["a"]
        field = result["f"]
        articles.append({
            "id": article["id"],
            "title": article["title"],
            "content": article["content"],
            "publication_date": article["publication_date"],
            "author": {"id": author["id"], "name": author["name"]} if author else None,
            "field": {"id": field["id"], "name": field["name"]} if field else None
        })
    return success_response(
        data=articles,
        message="Articles retrieved successfully"
    ), 200

@article_bp.route("/articles/<article_id>", methods=["GET"])
def get_article(article_id):
    model = ArticleModel()
    result = model.get_article(article_id)
    if result:
        article = result["p"]
        author = result["a"]
        field = result["f"]
        return success_response(
            data={
                "id": article["id"],
                "title": article["title"],
                "content": article["content"],
                "publication_date": article["publication_date"],
                "author": {"id": author["id"], "name": author["name"]} if author else None,
                "field": {"id": field["id"], "name": field["name"]} if field else None
            },
            message="Article retrieved successfully"
        ), 200
    return error_response("Article not found", 404)

@article_bp.route("/articles/<article_id>", methods=["PUT"])
def update_article(article_id):
    data = request.get_json()
    required_fields = ["title", "content", "publication_date", "author_id", "field_id"]
    if not data or not all(field in data for field in required_fields):
        return error_response("Missing required fields", 400)
    
    model = ArticleModel()
    result = model.get_article(article_id)
    if not result:
        return error_response("Article not found", 404)
    
    result = model.update_article(
        article_id,
        data["title"],
        data["content"],
        data["publication_date"],
        data["author_id"],
        data["field_id"]
    )
    if result:
        article = result["p"]
        author = result["a"]
        field = result["f"]
        return success_response(
            data={
                "id": article["id"],
                "title": article["title"],
                "content": article["content"],
                "publication_date": article["publication_date"],
                "author": {"id": author["id"], "name": author["name"]},
                "field": {"id": field["id"], "name": field["name"]}
            },
            message="Article updated successfully"
        ), 200
    return error_response("Failed to update article", 500)

@article_bp.route("/articles/<article_id>", methods=["DELETE"])
def delete_article(article_id):
    model = ArticleModel()
    result = model.get_article(article_id)
    if not result:
        return error_response("Article not found", 404)
    
    model.delete_article(article_id)
    return success_response(message="Article deleted successfully"), 200