from flask import Flask
from flask_restx import Api
from APIClasses.BlogAPI import *
from APIClasses.LikeAPI import *
from DataBaseDir.DataBase import *
from APIClasses.RegistrationAPI import *
from APIClasses.AuthenticationAPI import *
from AuthenticationMethods.Authenticate import authenticate
from APIClasses.PostAPI import *
from flask_swagger_ui import get_swaggerui_blueprint


app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret-key'
api = Api(app)
engine = DataBase().engine

# Swagger specific. Please go to http://127.0.0.1:5000/documentation/#/ for full documentation
SWAGGER_URL = '/documentation'
API_URL = '/static/APIDocumentation.yaml'
SWAGGERUI_BLUEPRINT = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={
        'app_name': "Dcoya's blogs website"
    }
)
app.register_blueprint(SWAGGERUI_BLUEPRINT, url_prefix=SWAGGER_URL)
# End swagger specific


@app.route('/login', methods=['POST'])
def authentication():
    return AuthenticationAPI().login(engine, app.config['SECRET_KEY'])


@app.route('/register', methods=['POST'])
def registration():
    return RegistrationApi().register(engine, "False")


@app.route('/registerposter', methods=['POST'])
def poster_registration():
    return RegistrationApi().register(engine, "True")


@app.route('/createblog', methods=['POST'])
@authenticate
def create_blog():
    return BlogAPI().create_blog(engine)


@app.route('/allblogs', methods=['GET'])
@authenticate
def get_all_blogs():
    return BlogAPI().get_all_blogs(engine)


@app.route('/addlike', methods=['POST'])
@authenticate
def add_like():
    return LikeAPI().add_like_to_post(engine)


@app.route('/removelike', methods=['DELETE'])
@authenticate
def remove_like():
    return LikeAPI().remove_like_from_post(engine)


@app.route('/createpost', methods=['POST'])
@authenticate
def create_post():
    return PostAPI().create_post(engine)


@app.route('/deletepost', methods=['DELETE'])
@authenticate
def delete_post():
    return PostAPI().delete_post(engine)


@app.route('/editpost', methods=['PUT'])
@authenticate
def edit_post():
    return PostAPI().edit_post(engine)


if __name__ == '__main__':
    app.run(debug=True)


