import models

from flask import Blueprint, request, jsonify
from flask_login import current_user
from playhouse.shortcuts import model_to_dict

painpoint = Blueprint('painpoint', 'painpoint', url_prefix='/painpoints')


# ================ SHOW ALL PAINPOINTS (PAINPOINT INDEX)================ #

@painpoint.route('/', methods=["GET"])
def get_all_painpoints():

    try:
        painpoint_categories = (models.Painpoint_Category
         .select(models.Painpoint_Category, models.Painpoint, models.Category)
         .join(models.Category)
         .switch(models.Painpoint_Category)
         .join(models.Painpoint)
         .order_by(models.Painpoint.date.desc())
         )


        returned_list = [model_to_dict(pp_and_c) for pp_and_c in painpoint_categories]

        ppc_list = []
        ids_so_far = []

        #return a list of dictionaries, with 'painpoint: {}' and 'categories: [...{}]' keys
        for dictionary in returned_list:
            painpoint_id = dictionary['painpoint']['id']

            if painpoint_id in ids_so_far:
                index_in_ppc_list = next((index for (index, dict) in enumerate(ppc_list) if dict['painpoint'] == dictionary['painpoint']), None)
                ppc_list[index_in_ppc_list]['categories'].append(dictionary['category'])

            else:
                ids_so_far.append(painpoint_id)
                ppc_list.append({'painpoint': dictionary['painpoint'], 'categories': [dictionary['category']]})

        return jsonify(data=ppc_list, status = {'code': 200, 'message': 'it should be working'})
    except models.DoesNotExist:
        return jsonify(data = {}, status = {'code': 401, 'message': 'Error getting all painpoints'})



# ================ CREATE PAINPOINT ================ #
@painpoint.route('/', methods=['POST'])
def create_painpoint():
    print('THIS IS REQUEST.GET_JSON', request.get_json())
    # payload = request.form.to_dict()
    payload = request.get_json()

    payload['owner'] = current_user.id
    print('THIS IS THE CURRENT_USER.ID', current_user.id)
    try:
        painpoint = models.Painpoint.create(**payload)

        painpoint_dict = model_to_dict(painpoint)
        print('THIS IS THE PAINPOINT DICT: ', painpoint_dict)
        return jsonify(data=painpoint_dict, status={'code': 201, 'message': 'successfully created painpoint'})


    except models.DoesNotExist:
        return jsonify(data=painpoint_dict, status={'code': 401, 'message': 'There was an error creating a painpoint'})



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
