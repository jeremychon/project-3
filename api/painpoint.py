import models

from flask import Blueprint, request, jsonify
from flask_login import current_user
from playhouse.shortcuts import model_to_dict

painpoint = Blueprint('painpoint', 'painpoint', url_prefix="/painpoints")


# # ================ SHOW ALL PAINPOINTS ================ #
# @api.route('/', methods=["GET"])
# def get_all_painpoints():
#     try:
#         painpoints = [model_to_dict(painpoint) for painpoint in models.Painpoint.select()]
#
#     except models.DoesNotExist:
#         return jsonify(data = {}, status = {'code': 401, 'message': 'Error getting all painpoints'})

# ================ CREATE PAINPOINT ================ #
@painpoint.route('/', methods=['POST'])
def create_painpoint():
    print('-----------Hitting create painpoint route-------------')
    payload = request.get_json()
    payload['owner_id'] = 1

    painpoint = models.Painpoint.create(**payload)

    painpoint_dict = model_to_dict(painpoint)

    return jsonify(data = painpoint_dict, status = {'code': 201, 'message': 'successfully created painpoint'})


# ================ SHOW PAINPOINT ================ #
@painpoint.route('/<id>', methods=['GET'])
def get_painpoint(id):
    painpoint = models.Painpoint.get_by_id(id)
    return jsonify(data=model_to_dict(painpoint), status={"code": 200, "message": "Success"})

# ================ UPDATE PAINPOINT ================ #
@painpoint.route('/<id>', methods = ['PUT'])
def update_painpoint(id):
    print('--------- Hitting update painpoint route ---------')

    payload = request.get_json()

    query = models.Painpoint.update(**payload).where(models.Painpoint.id == id)
    query.execute()

    updated_painpoint = models.Painpoint.get_by_id(id)

    return jsonify(data = model_to_dict(updated_painpoint), status = {"code": 200, "message": "Success"})



# ================ DELETE PAINPOINT ================ #
@painpoint.route('/<id>', methods = ['DELETE'])
def delete_painpoint(id):
    query = models.Painpoint.delete().where(models.Painpoint.id == id)
    query.execute()

    return jsonify(data = 'painpoint successfully deleted', status = {'code': 200, 'message': 'Painpoint successfully deleted'})


# # ================ PAINPOINT VOTE ================ #
# @painpoint.route('/<voter_id>/vote', methods=['POST'])
# def change_painpoint_vote(voter_id):
# 	payload = request.get_json()
#     payload['voter_id'] = current_user.voter_id
#     payload['post_id'] = int(voter_id)
#
# 		vote = models.Painpoint_Votes.create(**payload)
# 		vote_dict = model_to_dict(vote)
#
# 		return jsonify(data=vote_dict, status={'code': 200, 'message': 'Painpoint vote success'})
