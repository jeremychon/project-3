import models

from flask import Blueprint, request, jsonify
from flask_login import current_user
from playhouse.shortcuts import model_to_dict


solution = Blueprint('solution', 'solution', url_prefix='/solution')

# ================ GET ALL SOLUTIONS ================ #
@solution.route('/', methods=['GET'])
def all_solutions():
	try:
		all_solutions = [model_to_dict(solution) for solution in models.Solution.select()]
		return jsonify(data=all_solutions, status={'code': 200, 'message': 'Showing all solutions'})
	except models.DoesNotExist:
		return jsonify(data={}, status={'code': 401, 'message': 'There was an error to show all the solutions'})

# ================ GET ALL SOLUTIONS FOR SPECIFIC PAINPOINT ================ #
@solution.route('/<id>', methods=['GET'])
def painpoint_solutions():
	try:
		painpoint_solutions = [model_to_dict(solution) for solution in models.Solution.select().where(models.Solution.painpoint == id)]

		return jsonify(data=painpoint_solutions, status={'code': 200, 'message': 'Showing all solutions'})
	except models.DoesNotExist:
		return jsonify(data={}, status={'code': 401, 'message': 'There was an error to show all the solutions'})

# ================ CREATE SOLUTION ================ #
@solution.route('/', methods=['POST'])
def create_solution():

	# get the idea that is associated with the solution

	print(current_user, '<--- current_user')
	# payload = request.form.to_dict()
	payload = request.get_json()
	payload['owner'] = current_user.id
	print(payload, '<--- payload in solution create route')

	try:
		solution = models.Solution.create(**payload)
		print(solution, '<--- solution in solution create route')

		solution_dict = model_to_dict(solution)
		print(solution_dict, '<---- solution_dict')

		return jsonify(data=solution_dict, status={'code': 200, 'message': 'Create solution successful'})

	except models.DoesNotExist:
		return jsonify(data={}, status={'code': 401, 'message': 'There was an error creating a solution'})



# ================ UPDATE SOLUTION ================ #
@solution.route('/<id>', methods=['PUT'])
def update_solution(id):
	payload = request.get_json()
	print(payload, '<--- payload in update solution route')

	try:
		query = models.Solution.update(**payload).where(models.Solution.id == id)
		query.execute()

		updated_solution = models.Solution.get_by_id(id)
		print(model_to_dict(updated_solution), '<--- updated solution after query executes')

		return jsonify(data=model_to_dict(updated_solution), status={'code': 200, 'message': 'Updated solution successfully'})
	except models.DoesNotExist:
		return jsonify(data={}, status={'code': 401, 'message': 'There was an error updating the solution'})


# ================ DELETE SOLUTION ================ #
@solution.route('/<id>', methods=['Delete'])
def delete_solution(id):
	try:
		query = models.Solution.delete().where(models.Solution.id == id)
		query.execute()

		return jsonify(data='Solution successfully deleted', status={'code': 200, 'message': 'Solution successfully deleted'})
	except models.DoesNotExist:
		return None


# ================ CHANGE VOTE ================ #
@solution.route('/<id>/vote', methods=['POST'])
def change_solution_rating(id):
	payload = request.get_json()
	print(payload, '<--- payload in solution vote')
	payload['voter'] = current_user.id
	payload['post'] = int(id)
	print(payload, '<--- payload in solution vote after adding ids')

	try:
		vote = models.Solution_Votes.create(**payload)
		print(vote, '<---- created vote')
		vote_dict = model_to_dict(vote)
		print(vote_dict, '<--- vote_dict')

		return jsonify(data=vote_dict, status={'code': 200, 'message': 'Solution vote success'})

	except models.DoesNotExist:
		return jsonify(data={}, status={'code': 401, 'message': 'There was an error changing the solution rating'})
