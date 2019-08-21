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


class Solution(Model):
	idea_id = IntegerField()
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
	date = DateTimeField(datetime.datetime.now)

	class Meta:
		database = DATABASE


def initialize():
	DATABASE.connect()
	DATABASE.create_tables([User, Solution, Solution_Votes], safe=True)
	DATABASE.close()
