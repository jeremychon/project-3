from peewee import *
from flask_login import UserMixin
import datetime

Painpoints_API_DB = SqliteDatabase('painpoint.sqlite')

class BaseModel(Model):
    class Meta:
        database = Painpoints_API_DB

class User(UserMixin, BaseModel):
	full_name = CharField()
	username = CharField()
	email = CharField()
	password = CharField()


class Painpoint(UserMixin, BaseModel):
	owner = ForeignKeyField(User)
	date = DateTimeField(default=datetime.datetime.now)
	head = CharField()
	body = TextField()
	attachment = CharField()

class Painpoint_Votes(BaseModel):
	voter = IntegerField()
	post = IntegerField()
	vote = SmallIntegerField()
	date = DateTimeField(default=datetime.datetime.now)

class Category(UserMixin, BaseModel):
	category = CharField()


class Painpoint_Category(BaseModel):
	category = ForeignKeyField(Category)
	painpoint = ForeignKeyField(Painpoint)


class Solution(BaseModel):
	painpoint = ForeignKeyField(Painpoint)
	owner = ForeignKeyField(User)
	date = DateTimeField(default=datetime.datetime.now)
	head = CharField()
	body = TextField()
	attachment = CharField()


class Solution_Votes(BaseModel):
	voter = ForeignKeyField(User)
	post = ForeignKeyField(Painpoint)
	vote = SmallIntegerField()
	date = DateTimeField(default=datetime.datetime.now)



def initialize():
	Painpoints_API_DB.connect()
	Painpoints_API_DB.create_tables([User, Solution, Solution_Votes, Category, Painpoint, Painpoint_Category, Painpoint_Votes], safe = True)
	Painpoints_API_DB.close()
