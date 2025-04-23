from flask import Blueprint, request
from models import FieldModel
from utils.response import success_response, error_response

field_bp = Blueprint("field", __name__)

@field_bp.route("/fields", methods=["POST"])
def create_field():
    data = request.get_json()
    if not data or "name" not in data:
        return error_response("Missing 'name' field", 400)
    
    model = FieldModel()
    result = model.create_field(data["name"])
    if result:
        field = result["f"]
        return success_response(
            data={"id": field["id"], "name": field["name"]},
            message="Field created successfully"
        ), 201
    return error_response("Failed to create field", 500)

@field_bp.route("/fields/<field_id>", methods=["GET"])
def get_field(field_id):
    model = FieldModel()
    result = model.get_field(field_id)
    if result:
        field = result["f"]
        return success_response(
            data={"id": field["id"], "name": field["name"]},
            message="Field retrieved successfully"
        ), 200
    return error_response("Field not found", 404)

@field_bp.route("/fields/<field_id>", methods=["PUT"])
def update_field(field_id):
    data = request.get_json()
    if not data or "name" not in data:
        return error_response("Missing 'name' field", 400)
    
    model = FieldModel()
    result = model.get_field(field_id)
    if not result:
        return error_response("Field not found", 404)
    
    result = model.update_field(field_id, data["name"])
    if result:
        field = result["f"]
        return success_response(
            data={"id": field["id"], "name": field["name"]},
            message="Field updated successfully"
        ), 200
    return error_response("Failed to update field", 500)

@field_bp.route("/fields/<field_id>", methods=["DELETE"])
def delete_field(field_id):
    model = FieldModel()
    result = model.get_field(field_id)
    if not result:
        return error_response("Field not found", 404)
    
    model.delete_field(field_id)
    return success_response(message="Field deleted successfully"), 200

@field_bp.route("/fields/search", methods=["GET"])
def search_by_name():
    name = request.args.get("name")
    if not name:
        return error_response("Name query parameter is required", 400)
    
    model = FieldModel()
    result = model.get_field_by_name(name)
    
    if result:
        field = result["f"]
        return success_response(
            data={
                "id": field["id"],
                "name": field["name"]
            },
            message="Field found successfully"
        ), 200
    return error_response("No fields found with that name", 404)