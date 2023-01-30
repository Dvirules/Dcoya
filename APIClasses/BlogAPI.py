from flask_restx import Resource, reqparse
from sqlalchemy.orm import sessionmaker
from DataBaseDir.DataBaseSchema import Blog, User
import jwt
from flask import request


class BlogAPI(Resource):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def create_blog(self, engine):
        parser = reqparse.RequestParser()
        parser.add_argument('blog_title', required=True)
        try:
            args = parser.parse_args()
        except Exception as e:
            return {"message": f"error {e}.. Please make sure you have sent all required data to create this blog: "
                               "blog_title"}, 400

        session = sessionmaker(bind=engine)()
        blogs = session.query(Blog).all()

        # Verify no such blog exists
        for blog in blogs:
            if blog.title == args.blog_title:
                return {"message": "A blog with this title already exists. Please choose a different title"}, 409

        # Find the requesting user from the cookie
        token = request.cookies.get('Authorization')
        payload = jwt.decode(token, "secret-key", "HS256")
        user = session.query(User).filter_by(username=payload['username']).first()
        session.add(Blog(title=args.blog_title, author=user, author_id=user.id))
        session.commit()
        session.close()
        return {"message": "Blog Created!"}, 200

    def get_all_blogs(self, engine):
        # Retrieve all blogs in the database
        session = sessionmaker(bind=engine)()
        blogs = session.query(Blog).all()

        if blogs is None:
            return {"message": "No blogs found"}, 404

        if not blogs:
            return {"message": "There are currently no blogs posted"}, 200

        blogs_dict = {}
        posts = []
        for blog in blogs:
            blogs_dict[blog.id] = {"Blog ID": blog.id, "Blog Title": blog.title,  "Author ID": blog.author_id, "Blog Posts": str(blog.posts)}
            posts.clear()

        session.close()
        return blogs_dict, 200

