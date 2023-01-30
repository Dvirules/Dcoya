from flask_restx import Resource, reqparse
from sqlalchemy.orm import sessionmaker
from DataBaseDir.DataBaseSchema import User


class RegistrationApi(Resource):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def register(self, engine, can_post):
        parser = reqparse.RequestParser()
        parser.add_argument('username', required=True)
        parser.add_argument('email', required=True)
        parser.add_argument('password', required=True)
        try:
            args = parser.parse_args()
        except Exception as e:
            return {"message": f"error {e}.. Please make sure you have sent all required data to add a user: "
                               "username, email and password"}, 400

        session = sessionmaker(bind=engine)()
        user = User(username=args.username, email=args.email, password=args.password, can_post=can_post)
        all_users = session.query(User).all()
        # Checks if the email or username inserted are not already taken
        for user_in_table in all_users:
            if user_in_table.email == user.email:
                return {"message": "This email is already in use. Please insert a different email address"}, 409
            if user_in_table.username == user.username:
                return {"message": "This user name is already in use. Please select a different user name"}, 409

        session.add(user)
        session.commit()
        session.close()
        return {"message": f"User has been added!"}, 200
