from flask import Blueprint, request
from models import AuthorModel
from utils.response import success_response, error_response

author_bp = Blueprint("author", __name__)

@author_bp.route("/authors", methods=["POST"])
def create_author():
    data = request.get_json()
    if not data or "name" not in data:
        return error_response("Missing 'name' field", 400)
    
    model = AuthorModel()
    result = model.create_author(data["name"])
    if result:
        author = result["a"]
        return success_response(
            data={"id": author["id"], "name": author["name"]},
            message="Author created successfully"
        ), 201
    return error_response("Failed to create author", 500)

@author_bp.route("/authors/<author_id>", methods=["GET"])
def get_author(author_id):
    model = AuthorModel()
    result = model.get_author(author_id)
    if result:
        author = result["a"]
        return success_response(
            data={"id": author["id"], "name": author["name"]},
            message="Author retrieved successfully"
        ), 200
    return error_response("Author not found", 404)

@author_bp.route("/authors/<author_id>", methods=["PUT"])
def update_author(author_id):
    data = request.get_json()
    if not data or "name" not in data:
        return error_response("Missing 'name' field", 400)
    
    model = AuthorModel()
    result = model.get_author(author_id)
    if not result:
        return error_response("Author not found", 404)
    
    result = model.update_author(author_id, data["name"])
    if result:
        author = result["a"]
        return success_response(
            data={"id": author["id"], "name": author["name"]},
            message="Author updated successfully"
        ), 200
    return error_response("Failed to update author", 500)

@author_bp.route("/authors/<author_id>", methods=["DELETE"])
def delete_author(author_id):
    model = AuthorModel()
    result = model.get_author(author_id)
    if not result:
        return error_response("Author not found", 404)
    
    model.delete_author(author_id)
    return success_response(message="Author deleted successfully"), 200

@author_bp.route("/authors/name/<name>", methods=["GET"])
def get_author_by_name(name):
    model = AuthorModel()
    result = model.get_authors_by_similar_name(name)
    if result:
        author = result["a"]
        return success_response(
            data={"id": author["id"], "name": author["name"]},
            message="Author retrieved successfully"
        ), 200
    return error_response("Author not found", 404)

@author_bp.route("/authors/search", methods=["GET"])
def search_by_similar_name():
    name = request.args.get("name")
    if not name:
        return error_response("Name query parameter is required", 400)
    
    model = AuthorModel()
    results = model.get_authors_by_similar_name(name)
    
    if results:
        authors_data = []
        for result in results:
            author = result["a"]
            authors_data.append({
                "id": author["id"],
                "name": author["name"]
            })
        return success_response(
            data=authors_data,
            message="Authors found successfully"
        ), 200
    return error_response("No authors found with similar name", 404)