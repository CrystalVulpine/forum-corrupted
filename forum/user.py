from flask import *
import time
from sqlalchemy import *
from sqlalchemy.orm import relationship, deferred, joinedload, lazyload, contains_eager
import bcrypt
from forum.__main__ import db
from forum.relationships import *

class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, default=None)
    password = db.Column(db.String, default=None)
    deleted = db.Column(db.Integer, default=0)
    banned = db.Column(db.Integer, default=0)
    banned_until = db.Column(db.Integer, default=0)
    spammer = db.Column(db.Integer, default=0)
    pw_banned = db.Column(db.Integer, default=0)
    admin = db.Column(db.Integer, default=0)
    creation_date = db.Column(db.Integer, default=0)
    email = db.Column(db.String, default=None)
    email_verified = db.Column(db.Integer, default=0)
    community_id = db.Column(db.Integer, default=0)
    post_score = db.Column(db.Integer, default=0)
    comment_score = db.Column(db.Integer, default=0)

    posts=relationship("Post", lazy="dynamic", primaryjoin="Post.author_id==User.id")
    comments=relationship("Comment", lazy="dynamic", primaryjoin="Comment.author_id==User.id")

    moderates=relationship("Moderator", lazy="dynamic")
    banned_from=relationship("Ban", lazy="dynamic")
    contributor_of=relationship("Contributor", lazy="dynamic")
    subscriptions=relationship("Subscription", lazy="dynamic")
    blocked=relationship("Block", lazy="dynamic")


    def __init__(self, **kwargs):
        salt = bcrypt.gensalt()
        kwargs["password"] = bcrypt.hashpw(kwargs["password"].encode('utf-8'), salt)
        kwargs["creation_date"] = int(time.time())
        super().__init__(**kwargs)

    def set_password(self, password):
        salt = bcrypt.gensalt()
        self.password = bcrypt.hashpw(password.encode('utf-8'), salt)

    def valid_password(self, password):
        if not self.pw_banned and bcrypt.checkpw(password.encode('utf-8'), self.password):
            return True
        return False

    @property
    def score(self):
        return post_score + comment_score

    @property
    def ban_expires(self):
        if self.banned_until > 0:
            return banned_until
        else:
            return False

    @classmethod
    def by_id(cls, id):
        return db.session.query(cls).get(id)

    @classmethod
    def get_user(cls, username):
        return db.session.query(cls).filter(func.lower(User.username) == func.lower(username)).first()

