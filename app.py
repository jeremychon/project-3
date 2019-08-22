from flask import Flask, g
from flask_cors import CORS
from flask_login import LoginManager
import models

# import blueprints
from api.user import user
from api.solution import solution
from api.category import category
from api.painpoint import painpoint


DEBUG = True
PORT = 8000

# sets up ability to set up the session
login_manager = LoginManager()

# Initializes an instance of the Flask class (aka starts the website)
app = Flask(__name__, static_url_path='', static_folder='static')


app.secret_key = 'FJkjewankl4@VDSAj'
login_manager.init_app(app)

@login_manager.user_loader
def load_user(userId):
	try:
		return models.User.get(models.User.id == userId)
	except models.DoesNotExist:
		return None

CORS(user, origins=['http://localhost:3000'], supports_credentials=True)
CORS(solution, origins=['http://localhost:3000'], supports_credentials=True)
CORS(category, origins=['http://localhost:3000'], supports_credentials=True)
CORS(painpoint, origins=['http://localhost:3000'], supports_credentials=True)

app.register_blueprint(user)
app.register_blueprint(solution)
app.register_blueprint(category)
app.register_blueprint(painpoint)


@app.before_request
def before_request():
	'''Connect to the database'''
	g.db = models.Painpoints_API_DB
	g.db.connect()

@app.after_request
def after_request(response):
	### Close the database after each request ###
	g.db.close()
	return response

# sets the default URL with a '/'
# comes before any other route
# This will be the sign in page
@app.route('/')
def index():
	return 'Pain Point'


if __name__ == '__main__':
	models.initialize()
	app.run(debug=DEBUG, port=PORT)
