from flask import Blueprint, request
from models import ArticleModel, AuthorModel, FieldModel
from utils.response import success_response, error_response

article_bp = Blueprint("article", __name__)

@article_bp.route("/articles", methods=["POST"])
def create_article():
    data = request.get_json()
    required_fields = ["title", "content", "author_id", "field_id", "type"]
    if not data or not all(field in data for field in required_fields):
        return error_response("Missing required fields", 400)
    
    model = ArticleModel()
    result = model.create_article(
        data["title"],
        data["content"],
        data["author_id"],
        data["field_id"],
        data["type"]
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
                "type": article["type"],
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
            "type": article["type"],
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
                "type": article["type"],
                "author": {"id": author["id"], "name": author["name"]} if author else None,
                "field": {"id": field["id"], "name": field["name"]} if field else None
            },
            message="Article retrieved successfully"
        ), 200
    return error_response("Article not found", 404)

@article_bp.route("/articles/<article_id>", methods=["PUT"])
def update_article(article_id):
    data = request.get_json()
    required_fields = ["title", "content", "author_id", "field_id", "type"]
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
        data["author_id"],
        data["field_id"],
        data["type"]
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
                "type": article["type"],
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

@article_bp.route("/articles/excel", methods=["POST"])
def create_articles_from_excel():
    if "file" not in request.files:
        return error_response("No file provided", 400)
    
    file = request.files["file"]
    if not file.filename.endswith('.xlsx'):
        return error_response("Invalid file format. Please upload an Excel file (.xlsx)", 400)

    try:
        import pandas as pd
        df = pd.read_excel(file)
        
        required_columns = ["title", "content", "author_name", "field_name", "type"]
        missing_columns = [col for col in required_columns if col not in df.columns]
        if missing_columns:
            return error_response(f"Missing required columns: {', '.join(missing_columns)}", 400)
        
        df = df.dropna(subset=required_columns)
        if df.empty:
            return error_response("No valid data found in the Excel file", 400)
        
        article_model = ArticleModel()
        author_model = AuthorModel()
        field_model = FieldModel()
        
        created_articles = []
        failed_articles = []

        for index, row in df.iterrows():
            try:
                author_name = str(row["author_name"]).strip()
                author_result = author_model.get_authors_by_similar_name(author_name)
                if not author_result:
                    author_result = author_model.create_author(author_name)
                    if not author_result:
                        failed_articles.append({"row": index + 2, "reason": "Failed to create author"})
                        continue
                author_id = author_result["id"]
                
                field_name = str(row["field_name"]).strip()
                field_result = field_model.get_field_by_name(field_name)
                if not field_result:
                    field_result = field_model.create_field(field_name)
                    if not field_result:
                        failed_articles.append({"row": index + 2, "reason": "Failed to create field"})
                        continue
                field_id = field_result["id"]

                title = str(row["title"]).strip()
                content = str(row["content"]).strip()
                article_type = str(row["type"]).strip()

                result = article_model.create_article(
                    title,
                    content,
                    author_id,
                    field_id,
                    article_type
                )
                
                if result:
                    article = result["p"]
                    author = result["a"]
                    field = result["f"]
                    created_articles.append({
                        "id": article["id"],
                        "title": article["title"],
                        "content": article["content"],
                        "type": article["type"],
                        "author": {"id": author["id"], "name": author["name"]},
                        "field": {"id": field["id"], "name": field["name"]}
                    })
                else:
                    failed_articles.append({"row": index + 2, "reason": "Failed to create article"})
                    
            except Exception as e:
                failed_articles.append({"row": index + 2, "reason": str(e)})
                continue

        if created_articles:
            return success_response(data={"created": created_articles, "failed": failed_articles}), 201
        else:
            return error_response("No articles were created. All rows failed."), 400
            
    except Exception as e:
        return error_response(f"Error processing Excel file: {str(e)}", 400)

@article_bp.route("/articles/title/<title>", methods=["GET"])
def get_article_by_title(title):
    model = ArticleModel()
    result = model.get_authors_by_similar_name(title)
    if result:
        article = result["p"]
        author = result.get("a", {})
        field = result.get("f", {})
        return success_response(
            data={
                "id": article["id"],
                "title": article["title"],
                "content": article["content"],
                "type": article["type"],
                "author": {"id": author.get("id"), "name": author.get("name")} if author else None,
                "field": {"id": field.get("id"), "name": field.get("name")} if field else None
            },
            message="Article retrieved successfully"
        ), 200
    return error_response("Article not found", 404)

@article_bp.route("/articles/search", methods=["POST"])
def search_by_name():
    data = request.get_json()
    if not data or "name" not in data:
        return error_response("Name parameter is required", 400)
    
    name = data["name"]
    model = ArticleModel()
    results = model.get_articles_by_similar_name(name)
    
    if results:
        articles_data = []
        for result in results:
            article = result["p"]
            author = result.get("a", {})
            field = result.get("f", {})
            articles_data.append({
                "id": article["id"],
                "title": article["title"],
                "content": article["content"],
                "type": article["type"],
                "author": {"id": author.get("id"), "name": author.get("name")} if author else None,
                "field": {"id": field.get("id"), "name": field.get("name")} if field else None
            })
        return success_response(
            data=articles_data,
            message="Articles found successfully"
        ), 200
    return error_response("No articles found with similar name", 404)
