from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from flask_restx import Resource
# Schema file for all classes in the DB

Base = declarative_base()


class Blog(Base, Resource):
    __tablename__ = 'blogs'
    id = Column(Integer, primary_key=True)
    title = Column(String(50))
    author_id = Column(Integer, ForeignKey('users.id'))
    author = relationship("User", back_populates="blogs")
    posts = relationship("Post", back_populates="blog")


class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    username = Column(String(20), unique=True, nullable=False)
    email = Column(String(30), unique=True, nullable=False)
    password = Column(String(30), nullable=False)
    can_post = Column(String, nullable=True)
    blogs = relationship("Blog", back_populates="author")
    posts = relationship("Post", back_populates="author")
    likes = relationship("Like", back_populates="user")
    comments = relationship("Comment", back_populates="user")


class Post(Base):
    __tablename__ = 'posts'
    id = Column(Integer, primary_key=True)
    title = Column(String(50), unique=True, nullable=False)
    content = Column(String(1000))
    author_id = Column(Integer, ForeignKey('users.id'))
    blog_id = Column(Integer, ForeignKey('blogs.id'))
    author = relationship("User", back_populates="posts")
    blog = relationship("Blog", back_populates="posts")
    likes = relationship("Like", back_populates="post")
    comments = relationship("Comment", back_populates="post")

    def __repr__(self):
        return "{" + f"Post ID - {self.id}, Post title - {self.title}, Post content - {self.content}," \
               f"Author ID - {self.author_id}, Blog ID - {self.blog_id}, Post likes - {len(self.likes)}" + "}"


class Like(Base, Resource):
    __tablename__ = 'likes'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    post_id = Column(Integer, ForeignKey('posts.id'))
    user = relationship("User", back_populates="likes")
    post = relationship("Post", back_populates="likes")


class Comment(Base):
    __tablename__ = 'comments'
    id = Column(Integer, primary_key=True)
    content = Column(String)
    user_id = Column(Integer, ForeignKey('users.id'))
    post_id = Column(Integer, ForeignKey('posts.id'))
    user = relationship("User", back_populates="comments")
    post = relationship("Post", back_populates="comments")
