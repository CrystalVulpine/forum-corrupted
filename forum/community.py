from flask import *
import time
from sqlalchemy import *
from sqlalchemy.orm import relationship, deferred, joinedload, lazyload, contains_eager
from forum.__main__ import db

class Community(db.Model):
    __tablename__ = "communities"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, default=None)
    title = db.Column(db.String, default=None)
    deleted = db.Column(db.Integer, default=0)
    banned = db.Column(db.Integer, default=0)
    locked = db.Column(db.Integer, default=0)
    mode = db.Column(db.String, default='public')
    creation_date = db.Column(db.Integer, default=0)
    creator_id = db.Column(db.Integer, default=0)
    description = db.Column(db.String, default=None)
    icon_url = db.Column(db.String, default=None)
    banner_url = db.Column(db.String, default=None)
    stylesheet = db.Column(db.String, default=None)

    posts=relationship("CommunityPost", lazy="dynamic")

    mods=relationship("Moderator", lazy="dynamic")
    banned=relationship("Ban", lazy="dynamic")
    contributors=relationship("Contributor", lazy="dynamic")
    subscribers=relationship("Subscription", lazy="dynamic")

    def __init__(self, **kwargs):
        kwargs["creation_date"] = int(time.time())
        super().__init__(**kwargs)

    @classmethod
    def get_community(cls, name):
        return db.session.query(cls).filter(func.lower(Community.name) == func.lower(name)).first()

    @classmethod
    def by_id(cls, id):
        return db.session.query(cls).get(id)

