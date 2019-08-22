import models

import os
import sys
import secrets
from PIL import Image

from flask import Blueprint, request, jsonify, url_for, send_file
# Blueprint -- they record operations to execute (their controllers)

from flask_bcrypt import generate_password_hash, check_password_hash
from flask_login import login_user, current_user, logout_user
from playhouse.shortcuts import model_to_dict


user = Blueprint('user', 'user', url_prefix='/user')


# ================ REGISTER ================ #
# def save_picture(form_picture):
# 	random_hex = secrets.token_hex(8)

# 	# returning an array of [jeremy, .png]
# 	f_name, f_ext = os.path.splitext(form_picture.filename)

# 	picture_name = random_hex + f_ext
# 	print(picture_name, '<--- picture_name')

# 	# creates the file path
# 	file_path_for_avatar = os.path.join(os.getcwd(), 'static/profile_pics/' + picture_name)

# 	# Pillow code
# 	output_size = (125, 175)

# 	# open file sent from client
# 	i = Image.open(form_picture)
# 	i.thumbnail(output_size)
# 	i.save(file_path_for_avatar)

# 	return picture_name


@user.route('/register', methods=['POST'])
def register():
	# pay_file = request.files

	# form info
	payload = request.get_json()
	print(payload, '<--- payload in user register route')
	# dict_file = pay_file.to_dict()
	# print(dict_file, '<--- dict_file')

	payload['email'].lower()

	try:
		models.User.get(models.User.email == payload['email'])

		return jsonify(data={}, status={'code': 401, 'message': 'A user with that username and/or email already exists'})

	except models.DoesNotExist:

		payload['password'] = generate_password_hash(payload['password'])

		# file_picture_path = save_picture(dict_file['file'])

		# payload['image'] = file_picture_path

		user = models.User.create(**payload)
		print(user, '<--- registered user')

		login_user(user)

		user_dict = model_to_dict(user)
		print(user_dict, '<--- user_dict in register route')

		del user_dict['password']

		return jsonify(data=user_dict, status={'code': 200, 'message': 'Register successful'})


# ================ SHOW ALL USERS ================ #
@user.route('/', methods=['GET'])
def show_all_users():
	try:
		all_users = [model_to_dict(user) for user in models.User.select()]

		return jsonify(data=all_users, status={'code': 200, 'message': 'All users are shown'})
	except models.DoesNotExist:
		return jsonify(data={}, status={'code': 401, 'message': 'There was an error getting the users'})


# ================ LOGIN ================ #
@user.route('/login', methods=['POST'])
def login():
	payload = request.get_json()
	print(payload, '<--- payload from login route')

	try:
		user = models.User.get(models.User.email == payload['email'])
		print(user, '<--- found user')
		user_dict = model_to_dict(user)
		print(user_dict, '<--- user_dict')

		if check_password_hash(user_dict['password'], payload['password']):
			del user_dict['password']
			login_user(user)

			return jsonify(data=user_dict, status={'code': 200, 'message': 'User successfully logged in'})
		else:
			return jsonify(data={}, status={'code': 401, 'message': 'Incorrect username and/or password'})

	except models.DoesNotExist:
		return jsonify(data={}, status={'code': 401, 'message': 'Incorrect username and/or password'})


# ================ GET USER INFO ================ #
@user.route('/<id>', methods=['GET'])
def get_user(id):
	try:
		user = models.User.get(models.User.id == id)
		print(user, '<--- user')
		user_dict = model_to_dict(user)
		print(user_dict, '<--- user_dict')

		all_painpoints = [model_to_dict(painpoint) for painpoint in models.Painpoint.select().where(models.Painpoint.owner_id == id)]
		# user['all_painpoints'] = all_painpoints

		all_solutions = [model_to_dict(solution) for solution in models.Solution.select().where(models.Solution.owner_id == id)]
		# user['all_solutions'] = all_solutions

		return jsonify(data=user_dict, status={'code': 200, 'message': 'User found'})

	except models.DoesNotExist:
		return jsonify(data={}, status={'code': 401, 'message': 'There was an error finding the user'})


# ================ DELETE USER ================ #
@user.route('/<id>', methods=['Delete'])
def delete_user(id):
	query = models.User.delete().where(models.User.id == id)
	query.execute()

	return jsonify(data='User account deleted', status={'code': 200, 'message': 'User has been deleted'})


# ================ UPDATE USER ================ #
@user.route('/<id>', methods=['PUT'])
def update_user(id):
	payload = request.get_json()

	try:
		query = models.User.update(**payload).where(models.User.id == id)
		query.execute()

		updated_user = models.User.get_by_id(id)

		return jsonify(data=model_to_dict(updated_user), status={'code': 200, 'message': 'User has been updated'})

	except models.DoesNotExist:
		return jsonify(data={}, status={'code': 401, 'message': 'There was an error updating the user'})


# ================ LOGOUT ================ #
@user.route('/logout', methods=['POST'])
def logout():
	logout_user()
	return 'You are logged out'
	# return redirect('http://localhost:8000/')
