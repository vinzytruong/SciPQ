from flask import jsonify

def success_response(data=None, message="Success"):
    response = {
        "status": "success",
        "message": message
    }
    if data is not None:
        response["data"] = data
    return jsonify(response)

def error_response(message="Error", status_code=400):
    return jsonify({
        "status": "error",
        "message": message
    }), status_code