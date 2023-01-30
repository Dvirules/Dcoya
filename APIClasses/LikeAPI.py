from flask import request
from flask_restx import Resource, reqparse
from sqlalchemy.orm import sessionmaker
from DataBaseDir.DataBaseSchema import Post, Like, User
import jwt


class LikeAPI(Resource):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def add_like_to_post(self, engine):
        parser = reqparse.RequestParser()
        parser.add_argument('post_title', required=True)
        try:
            args = parser.parse_args()
        except Exception as e:
            return {"message": f"error {e}.. Please make sure you have sent all required data to like a post: "
                               "post_title"}, 400

        # Check for the post
        session = sessionmaker(bind=engine)()
        post = session.query(Post).filter_by(title=args.post_title).first()
        if not post:
            return {"message": "Post not found"}, 404

        token = request.cookies.get('Authorization')
        payload = jwt.decode(token, "secret-key", "HS256")
        username = payload['username']
        user = session.query(User).filter_by(username=username).first()
        # Check for the user
        if not user:
            return {"message": "No such user exists"}, 404

        # Check if the user didn't already like this post
        for like_in_post in post.likes:
            if like_in_post.user == user:
                return {
                    "message": "You have already liked this post"}, 403

        like = Like(post=post, user=user)
        session.add(like)
        session.commit()
        return_payload = {'message': f'Like with the ID of {like.id} added to post with the ID of {post.id} - {post.title}'}, 201
        session.close()

        return return_payload

    def remove_like_from_post(self, engine):
        parser = reqparse.RequestParser()
        parser.add_argument('post_id', required=True)
        parser.add_argument('like_id', required=True)
        try:
            args = parser.parse_args()
        except Exception as e:
            return {"message": f"error {e}.. Please make sure you have sent all required data to delete this like: "
                               "post_id and like_id"}, 400

        session = sessionmaker(bind=engine)()
        post = session.query(Post).filter_by(id=args.post_id).first()
        # Check for the post
        if not post:
            return {"message": "Post not found"}, 404

        like = session.query(Like).filter_by(id=args.like_id).first()
        # Check for the like
        if not like:
            return {"message": "Like has already been removed, or never existed"}, 404

        token = request.cookies.get('Authorization')
        payload = jwt.decode(token, "secret-key", "HS256")
        username = payload['username']
        user = session.query(User).filter_by(username=username).first()
        # Check for the user
        if not user:
            return {"message": "No such user exists"}, 404

        if like not in user.likes:
            return {"message": "Insufficient permissions for selected user to perform this operation as you are not the like creator"}, 403

        session.delete(like)
        session.commit()
        session.close()
        return {'message': 'Like removed'}, 200
