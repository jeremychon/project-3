from peewee import * 
from flask_login import UserMixin
import datetime

DATABASE = SqliteDatabase('painpoint.sqlite')