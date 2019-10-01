import models

from flask import Blueprint, request, jsonify
from playhouse.shortcuts import model_to_dict # from peewee

category = Blueprint('category', 'category', url_prefix="/category")


@category.route('/', methods=["GET"])
def get_category():
    try:
        category = [model_to_dict(category) for category in models.Category.select()]
        return jsonify(data=category, status={"code": 200, "message": "Success"})
    except models.DoesNotExist:
        return jsonify(data={}, status={"code": 401, "message": " There was an error getting the resource"})

@category.route('/', methods=["POST"])
def create_category():
    payload = request.get_json()

    category = models.Category.create(**payload)
    category_dict = model_to_dict(category)

    return jsonify(data = category_dict, status = {"code": 201, "message": "Create successful"})
