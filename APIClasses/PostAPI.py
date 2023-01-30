import jwt
from flask import request, abort
from flask_restx import Resource, reqparse
from sqlalchemy.orm import sessionmaker
from DataBaseDir.DataBaseSchema import Post, User, Blog


class PostAPI(Resource):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    # This Method checks whether the user making the request is a poster user (a user with sufficient permissions to post a blog post) or not
    def is_user_a_poster(self):
        token = request.cookies.get('Authorization')
        payload = jwt.decode(token, "secret-key", "HS256")
        if payload['can_post'] == 'True':
            return True
        else:
            return False

    # This Method checks whether the user making the request is the poster (author) of the specific post in the request
    def is_user_post_creator(self, engine, post_title):
        session = sessionmaker(bind=engine)()
        post = session.query(Post).filter_by(title=post_title).first()

        if not post:
            return abort(404, description=f"No post with the title of {post_title} is found")

        token = request.cookies.get('Authorization')
        payload = jwt.decode(token, "secret-key", "HS256")

        user = session.query(User).filter_by(username=payload['username']).first()
        if user.id == post.author_id:
            return True
        else:
            return False

    def create_post(self, engine):
        if self.is_user_a_poster():
            parser = reqparse.RequestParser()
            parser.add_argument('post_title', required=True)
            parser.add_argument('post_content', required=True)
            parser.add_argument('blog_id', required=True)
            try:
                args = parser.parse_args()
            except Exception as e:
                return {"message": f"error {e}.. Please make sure you have sent all required data to create this post: "
                                   "post_title, post_content and blog_id"}, 400

            session = sessionmaker(bind=engine)()
            token = request.cookies.get('Authorization')
            payload = jwt.decode(token, "secret-key", "HS256")
            user = session.query(User).filter_by(username=payload['username']).first()
            blog = session.query(Blog).filter_by(id=args.blog_id).first()
            if not blog:
                return {"message": f"No blog with the ID of {args.blog_id} is found"}, 404

            all_posts = session.query(Post).all()
            for post_in_db in all_posts:
                if post_in_db.title == args.post_title:
                    return {"message": "A post with this title already exists. Please choose a different title"}, 409

            post = Post(title=args.post_title, content=args.post_content, author_id=user.id, blog=blog)
            session.add(post)
            session.commit()
            session.close()
            return {'message': 'Your Post Has been added'}, 201

        else:
            return abort(403, description="You do not have the sufficient permissions to create a post!")

    def delete_post(self, engine):
        if self.is_user_a_poster():
            parser = reqparse.RequestParser()
            parser.add_argument('post_title', required=True)
            try:
                args = parser.parse_args()
            except Exception as e:
                return {"message": f"error {e}.. Please make sure you have sent all required data to delete this post: "
                                   "post_title"}, 400

            if self.is_user_post_creator(engine, args.post_title):
                session = sessionmaker(bind=engine)()
                post = session.query(Post).filter_by(title=args.post_title).first()

                if not post:
                    return {"message": "Post not found"}, 404

                session.delete(post)
                session.commit()
                session.close()
                return {'message': 'The selected post has been deleted'}, 200
            else:
                return abort(403, description="You do not have the sufficient permissions to delete this post, as you are not its author")

        else:
            return abort(403, description="You do not have the sufficient permissions to delete a post!")

    def edit_post(self, engine):
        if self.is_user_a_poster():
            parser = reqparse.RequestParser()
            parser.add_argument('post_title', required=True)
            parser.add_argument('new_content', required=True)
            try:
                args = parser.parse_args()
            except Exception as e:
                return {"message": f"error {e}.. Please make sure you have sent all required data to edit this post: "
                                   "post_title and new_content"}, 400

            if self.is_user_post_creator(engine, args.post_title):
                session = sessionmaker(bind=engine)()
                post = session.query(Post).filter_by(title=args.post_title).first()
                post.content = args.new_content
                session.commit()
                session.close()
                return {'message': f'Your selected post has been edited'}, 200
            else:
                return abort(403, description="You do not have the sufficient permissions to edit this post, as you are not its author")

        else:
            return abort(403, description="You do not have the sufficient permissions to edit a post!")
