from flask import Blueprint, request
from models import AuthorModel
from utils.response import success_response, error_response

author_bp = Blueprint("author", __name__)

@author_bp.route("/authors", methods=["POST"])
def create_author():
    try:
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
        return error_response("Failed to create author due to internal error", 500)
    except Exception as e:
        return error_response(f"Server error: {str(e)}", 500)


@author_bp.route("/authors/<author_id>", methods=["GET"])
def get_author(author_id):
    try:
        model = AuthorModel()
        result = model.get_author(author_id)
        if result:
            author = result["a"]
            return success_response(
                data={"id": author["id"], "name": author["name"]},
                message="Author retrieved successfully"
            ), 200
        return error_response(f"No author found with ID {author_id}", 404)
    except Exception as e:
        return error_response(f"Server error: {str(e)}", 500)


@author_bp.route("/authors/<author_id>", methods=["PUT"])
def update_author(author_id):
    try:
        data = request.get_json()
        if not data or "name" not in data:
            return error_response("Missing 'name' field", 400)

        model = AuthorModel()
        result = model.get_author(author_id)
        if not result:
            return error_response(f"No author found with ID {author_id}", 404)

        result = model.update_author(author_id, data["name"])
        if result:
            author = result["a"]
            return success_response(
                data={"id": author["id"], "name": author["name"]},
                message="Author updated successfully"
            ), 200
        return error_response("Failed to update author due to internal error", 500)
    except Exception as e:
        return error_response(f"Server error: {str(e)}", 500)


@author_bp.route("/authors/<author_id>", methods=["DELETE"])
def delete_author(author_id):
    try:
        model = AuthorModel()
        result = model.get_author(author_id)
        if not result:
            return error_response(f"No author found with ID {author_id}", 404)

        model.delete_author(author_id)
        return success_response(message="Author deleted successfully"), 200
    except Exception as e:
        return error_response(f"Server error: {str(e)}", 500)


@author_bp.route("/authors", methods=["GET"])
def get_all_fields():
    try:
        model = AuthorModel()
        results = model.get_all_authors()

        authors = [{"id": author["f"]["id"], "name": author["f"]["name"]} for author in results] if results else []
        return success_response(
            data=authors,
            message="Authors retrieved successfully"
        ), 200
    except Exception as e:
        return error_response(f"Server error: {str(e)}", 500)



@author_bp.route("/authors/name/<name>", methods=["GET"])
def get_author_by_name(name):
    try:
        model = AuthorModel()
        result = model.get_authors_by_similar_name(name)
        if result:
            author = result["a"]
            return success_response(
                data={"id": author["id"], "name": author["name"]},
                message="Author retrieved successfully"
            ), 200
        return error_response(f"No author found with name similar to '{name}'", 404)
    except Exception as e:
        return error_response(f"Server error: {str(e)}", 500)


@author_bp.route("/authors/search", methods=["GET"])
def search_by_similar_name():
    try:
        name = request.args.get("name")
        if not name:
            return error_response("Query parameter 'name' is required", 400)

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
        return error_response(f"No authors found with name similar to '{name}'", 404)
    except Exception as e:
        return error_response(f"Server error: {str(e)}", 500)
