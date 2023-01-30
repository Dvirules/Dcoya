import datetime
from flask_restx import Resource
from sqlalchemy.orm import sessionmaker
import jwt
from flask import request, make_response, jsonify
from DataBaseDir.DataBaseSchema import User


class AuthenticationAPI(Resource):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def login(self, engine, key):
        # Get the user's credentials from the request
        username = request.json.get('username')
        password = request.json.get('password')

        session = sessionmaker(bind=engine)()
        user = session.query(User).filter_by(username=username).first()
        all_users = session.query(User).all()

        # Verify the user's credentials
        for user_in_table in all_users:
            if user_in_table.username == username and user_in_table.password == password:
                # Create a JWT token for the user if it was found
                payload = {'username': username,
                           'exp': datetime.datetime.utcnow() + datetime.timedelta(days=1),
                           'can_post': user.can_post}
                token = jwt.encode(payload, key, "HS256")
                response = make_response(jsonify({"message": "User successfully logged in!"}), 200)
                response.set_cookie('Authorization', token)
                return response
        else:
            return {'error': 'Invalid credentials'}, 401
