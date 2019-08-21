from peewee import *
from flask_login import UserMixin
import datetime

DATABASE = SqliteDatabase('painpoint.sqlite')


class User(UserMixin, Model):
	full_name = CharField()
	username = CharField()
	email = CharField()
	password = CharField()
	karma = CharField()

	class Meta:
		database = DATABASE

class Painpoint(UserMixin, Model):
	owner_id = IntegerField()
	date = DateTimeField(default=datetime.datetime.now)
	head = CharField()
	body = TextField()
	attachment = CharField()

	class Meta:
		database = DATABASE

class Painpoint_Votes(Model):
	voter_id = IntegerField()
	post_id = IntegerField()
	vote = SmallIntegerField()
	date = DateTimeField(default=datetime.datetime.now)

	class Meta:
		database = DATABASE


class Category(UserMixin, Model):
	category = CharField()

	class Meta:
		database = DATABASE

class Painpoint_Categories(Model):
	category_id: ForeignKeyField(Category)
	painpoint_id: ForeignKeyField(Painpoint)

	class Meta:
		database = DATABASE

class Solution(Model):
	painpoint_id = IntegerField()
	owner_id = IntegerField()
	date = DateTimeField(default=datetime.datetime.now)
	head = CharField()
	body = TextField()
	attachment = CharField()

	class Meta:
		database = DATABASE


class Solution_Votes(Model):
	voter_id = IntegerField()
	post_id = IntegerField()
	vote = SmallIntegerField()
	date = DateTimeField(default=datetime.datetime.now)

	class Meta:
		database = DATABASE


def initialize():
	DATABASE.connect()
	DATABASE.create_tables([User, Solution, Solution_Votes, Category, Painpoint, Painpoint_Categories, Painpoint_Votes], safe=True)
	DATABASE.close()
