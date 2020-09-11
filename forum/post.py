from flask import *
import time
from sqlalchemy import *
from sqlalchemy.orm import relationship, deferred, joinedload, lazyload, contains_eager
from forum.__main__ import db
from forum.relationships import *

class Post(db.Model):
    __tablename__ = "posts"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, default=None)
    url = db.Column(db.String, default=None)
    body = db.Column(db.String, default=None)
    author_id = Column(db.Integer, ForeignKey("users.id"))
    deleted = db.Column(db.Integer, default=0)
    creation_date = db.Column(db.Integer, default=0)
    edited_date = db.Column(db.Integer, default=0)
    ups = db.Column(db.Integer, default=1)
    downs = db.Column(db.Integer, default=0)
    admin_nuked = db.Column(db.Boolean, default=False)
    admin_removal = db.Column(db.String, default=None)

    communities=relationship("CommunityPost", lazy="dynamic")
    comments=relationship("Comment", lazy="dynamic", primaryjoin="Comment.post_id==Post.id")


    def __init__(self, **kwargs):
        kwargs["creation_date"] = int(time.time())
        super().__init__(**kwargs)

    def delete(self):
        self.deleted = True
        self.title = '[Deleted post]'
        self.url = ''
        self.body = ''
        self.author_id = 0
        db.session.commit()

    @property
    def score(self):
        return ups - downs

    @property
    def author(self):
        import forum.user as user
        return user.User.by_id(self.author_id)

    @classmethod
    def by_id(cls, id):
        return db.session.query(cls).get(id)

