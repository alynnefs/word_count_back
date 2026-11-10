from flask import Blueprint, jsonify, request

from app.counter import count_words
from app.validators import validate_count_request

bp = Blueprint("main", __name__)


@bp.route("/count", methods=["POST"])
def post_count():
    data = request.get_json(silent=True)
    try:
        validate_count_request(data)
    except OverflowError as e:
        return jsonify({"error": str(e)}), 413
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    return jsonify({"count": count_words(data["text"])}), 200


@bp.route("/count/", methods=["GET"])
@bp.route("/count/<text>", methods=["GET"])
def get_count(text=""):
    return str(count_words(text)), 200
