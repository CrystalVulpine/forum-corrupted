from flask import *
import time
from sqlalchemy import *
from sqlalchemy.orm import relationship, deferred, joinedload, lazyload, contains_eager
from forum.__main__ import db
from forum.relationships import *

class Post(db.Model):
    __tablename__ = "posts"
    id = Column(Integer, primary_key=True)
    title = Column(String, default=None)
    url = Column(String, default=None)
    body = Column(String, default=None)
    author_id = Column(Integer, ForeignKey("users.id"))
    deleted = Column(Boolean, default=False)
    creation_date = Column(Integer, default=0)
    edited_date = Column(Integer, default=0)
    ups = Column(Integer, default=1)
    downs = Column(Integer, default=0)
    admin_nuked = Column(Boolean, default=False)
    admin_removal = Column(String, default=None)

    communities=relationship("CommunityPost", lazy="dynamic")
    comments=relationship("Comment", lazy="dynamic", primaryjoin="Comment.post_id==Post.id")
    author=relationship("User", lazy="joined")


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

    def can_view(self, user):
        if user and user.admin >= 1:
            return True
        if self.admin_nuked:
            return False
        cp = self.communities.first()
        if not cp: 
            return True
        fc = cp.community
        if fc.mode == "private" and (not user or (not fc.contributors.filter_by(user_id = user.id).first() and not fc.mods.filter_by(user_id = user.id).first())):
            return False
        return True

    def posted_in(self, user):
        cps = self.communities.all()
        returns = []
        for cp in cps:
            if cp.removed and self.author_id != user.id:
                continue
            if not cp.community.can_view(user):
                continue            
            returns.append(cp)
        return returns

    @property
    def score(self):
        return ups - downs

    @classmethod
    def by_id(cls, id):
        return db.session.query(cls).get(id)

