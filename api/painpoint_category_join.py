import models

from flask import Blueprint, request, jsonify
from flask_login import current_user
from playhouse.shortcuts import model_to_dict

pp = Blueprint('pp_join', 'pp_join', url_prefix="/pp_cat_join/")

@pp.route('/', methods=['POST'])
def pp_cat_join():
    payload = request.get_json()

    pp_cat =  models.Painpoint_Category.create(**payload)

    pp_cat_dict = model_to_dict(pp_cat)

    return jsonify(data = pp_cat_dict, status={'code': 201, 'message': 'successfully created painpoint'})
