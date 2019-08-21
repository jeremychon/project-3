import models

from flask import Blueprint, request, jsonify
from playhouse.shortcuts import model_to_dict


solution = Blueprint('solution', 'solution', url_prefix='/solution')


# ================ CREATE ================ #
@solution.route('/', methods=['POST'])
def create_solution():

	payload = request.get_json()
	print(payload, '<--- payload in solution create route')

	try:
		solution = models.Solution.create(**payload)

		solution_dict = model_to_dict(solution)

		return jsonify(data=solution_dict, status={'code': 200, 'message': 'Create solution successful'})

	except models.DoesNotExist:
		return jsonify(data={}, status={'code': 401, 'message': 'There was an error creating a solution'})
