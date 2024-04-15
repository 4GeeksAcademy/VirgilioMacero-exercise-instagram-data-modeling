import os
import sys
from sqlalchemy import Column, ForeignKey, Integer, String, Table
from sqlalchemy.orm import relationship, declarative_base
from sqlalchemy import create_engine
from eralchemy2 import render_er

Base = declarative_base()

follower = Table(
    "follower",
    Base.metadata,
    Column("user_from_id", Integer, ForeignKey("user.id")),
    Column("user_to_id", Integer, ForeignKey("user.id")),
)

class User(Base):
    __tablename__ = "user"
    id = Column(Integer, primary_key=True)
    username = Column(String(250), nullable=False, unique=True)
    firstname = Column(String(250), nullable=False)
    lastname = Column(String(250), nullable=False)
    followers = relationship(
        "User",
        secondary=follower,
        primaryjoin=id == follower.c.user_to_id,
        secondaryjoin=id == follower.c.user_from_id,
        backref="following",
    )
    posts = relationship('Post',backref="user")
    comments = relationship("Comment",backref='user')



class Post(Base):
    __tablename__ = "post"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("user.id"))
    user = relationship(User)
    medias = relationship("Media",backref='post')
    comments = relationship("Comment",backref='post')

    def to_dict(self):
        return {}
    
class Media(Base):
    __tablename__ = "media"
    id = Column(Integer, primary_key=True)
    type = Column(Integer,nullable=True)
    url = Column(String(120),nullable=True)
    post_id = Column(Integer, ForeignKey("post.id"))
    post = relationship(Post)

    def to_dict(self):
        return {}
    
class Comment(Base):
    __tablename__ = "comment"
    id = Column(Integer, primary_key=True)
    comment_text = Column(String,nullable=True)
    author_id = Column(Integer, ForeignKey("user.id"))
    user = relationship(User)
    post_id = Column(Integer, ForeignKey("post.id"))
    post = relationship(Post)

    def to_dict(self):
        return {}


## Draw from SQLAlchemy base
try:
    result = render_er(Base, "diagram.png")
    print("Success! Check the diagram.png file")
except Exception as e:
    print("There was a problem genering the diagram")
    raise e
