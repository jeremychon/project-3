from flask import Flask, g
from flask_cors import CORS
from flask_login import LoginManager


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

app.register_blueprint(user)


@app.before_request
def before_request():
	'''Connect to the database'''
	g.db = models.DATABASE
	g.db.connect()

@app.after_request
def after_request():
	### Close the database after each request ###
	g.db.close()
	return response

# sets the default URL with a '/'
# comes before any other route
@app.route('/')


if __name__ == '__main__':
	models.initialize()
	app.run(debug=DEBUG, port=PORT)