import models

from flask import Blueprint, request, jsonify
from flask_login import current_user
from playhouse.shortcuts import model_to_dict

painpoint = Blueprint('painpoint', 'painpoint', url_prefix="/painpoints")

# # ================ JOIN PAINPOINTS AND categories================ #
# @painpoint.route('/pp_cat_join/<painpoint_id>', methods = ['POST']):
#     painpoint_categories = (Category
#     .select()
#     .join(Painpoint_Category)
#     .join(Painpoint)
#      .where(Painpoint.id == painpoint_id))
#ß
# for category in painpoint_categories:
#     print(category.category)

# ================ SHOW ALL PAINPOINTS (PAINPOINT INDEX)================ #
@painpoint.route('/', methods=["GET"])
def get_all_painpoints():
    try:
        painpoint_categories = (models.Painpoint_Category
         .select(models.Painpoint_Category, models.Painpoint, models.Category)
         .join(models.Category)
         .switch(models.Painpoint_Category)
         .join(models.Painpoint)
         )

        them = [model_to_dict(thing) for thing in painpoint_categories]
        print(them)

        return jsonify(data=them, status = {'code': 200, 'message': 'Got all painpoints'})

        # return 'check terminal'
    except models.DoesNotExist:
        return jsonify(data = {}, status = {'code': 401, 'message': 'Error getting all painpoints'})




# ================ CREATE PAINPOINT ================ #
@painpoint.route('/', methods=['POST'])
def create_painpoint():
    payload = request.get_json()
    print('here is payload')
    payload['owner'] = current_user.id
    print(payload)

    painpoint = models.Painpoint.create(**payload)

    painpoint_dict = model_to_dict(painpoint)

    return jsonify(data=painpoint_dict, status={'code': 201, 'message': 'successfully created painpoint'})


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
# @painpoint.route('/<voter>/vote', methods=['POST'])
# def change_painpoint_vote(voter):
# 	payload = request.get_json()
#     payload['voter'] = current_user.voter
#     payload['post'] = int(voter)
#
# 		vote = models.Painpoint_Votes.create(**payload)
# 		vote_dict = model_to_dict(vote)
#
# 		return jsonify(data=vote_dict, status={'code': 200, 'message': 'Painpoint vote success'})
