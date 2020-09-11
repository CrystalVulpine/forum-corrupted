from flask import *
import time
from sqlalchemy import *
from sqlalchemy.orm import relationship, deferred, joinedload, lazyload, contains_eager
from forum.__main__ import db

class Moderator(db.Model):
    __tablename__ = "mods"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    community_id = Column(Integer, ForeignKey("communities.id"))
    creation_date = Column(Integer, default=0)

    user=relationship("User", lazy="joined")
    community=relationship("Community", lazy="joined")

    def __init__(self, *args, **kwargs):
        kwargs["creation_date"] = int(time.time())
        super().__init__(*args, **kwargs)

    def __repr__(self):
        return f"<Mod(id={self.id}, user_id={self.user_id}, community_id={self.community_id})>"

class Contributor(db.Model):
    __tablename__ = "contributors"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    community_id = Column(Integer, ForeignKey("communities.id"))
    creation_date = Column(Integer, default=0)

    user=relationship("User", lazy="joined")
    community=relationship("Community", lazy="joined")

    def __init__(self, *args, **kwargs):
        kwargs["creation_date"] = int(time.time())
        super().__init__(*args, **kwargs)

    def __repr__(self):
        return f"<Contributor(id={self.id}, user_id={self.user_id}, community_id={self.community_id})>"

class Ban(db.Model):
    __tablename__ = "bans"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    community_id = Column(Integer, ForeignKey("communities.id"))
    creation_date = Column(Integer, default=0)
    expiration_date = Column(Integer, default=0)

    user=relationship("User", lazy="joined")
    community=relationship("Community", lazy="joined")

    def __init__(self, *args, **kwargs):
        kwargs["creation_date"] = int(time.time())
        super().__init__(*args, **kwargs)

    def __repr__(self):
        return f"<Ban(id={self.id}, user_id={self.user_id}, community_id={self.community_id})>"

class Subscription(db.Model):
    __tablename__ = "subscriptions"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    community_id = Column(Integer, ForeignKey("communities.id"))

    user=relationship("User", lazy="joined")
    community=relationship("Community", lazy="joined")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def __repr__(self):
        return f"<Subscription(id={self.id}, user_id={self.user_id}, community_id={self.community_id})>"

class Block(db.Model):
    __tablename__ = "blocks"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    community_id = Column(Integer, ForeignKey("communities.id"))

    user=relationship("User", lazy="joined")
    community=relationship("Community", lazy="joined")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def __repr__(self):
        return f"<Block(id={self.id}, user_id={self.user_id}, community_id={self.community_id})>"

class CommunityPost(db.Model):
    __tablename__ = "post_communities"
    id = Column(Integer, primary_key=True)
    post_id = Column(Integer, ForeignKey("posts.id"))
    community_id = Column(Integer, ForeignKey("communities.id"))
    removed = Column(Boolean, default=False)
    removed_by = Column(Integer, default=0)
    removal_reason = Column(String, default='spam')
    locked = Column(Boolean, default=False)
    approved = Column(Boolean, default=False)
    flair = Column(String, default=None)

    post=relationship("Post", lazy="joined")
    community=relationship("Community", lazy="joined")
    comments=relationship("CommunityComment", lazy="dynamic", primaryjoin="CommunityComment.cpost_id==CommunityPost.id")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    @property
    def community(self):
        import forum.community as community
        return community.Community.by_id(self.community_id)

    def __repr__(self):
        return f"<CommunityPost(id={self.id}, post_id={self.post_id}, community_id={self.community_id})>"

class CommunityComment(db.Model):
    __tablename__ = "comment_communities"
    id = Column(Integer, primary_key=True)
    comment_id = Column(Integer, ForeignKey("comments.id"))
    community_id = Column(Integer, ForeignKey("communities.id"))
    post_id = Column(Integer, ForeignKey("posts.id"))
    removed = Column(Boolean, default=False)
    removed_by = Column(Integer, default=0)
    removal_reason = Column(String, default='spam')
    locked = Column(Boolean, default=False)
    approved = Column(Boolean, default=False)

    comment=relationship("Comment", lazy="joined")
    community=relationship("Community", lazy="joined")
    cpost_id = Column(Integer, ForeignKey("post_communities.id"))
    post=relationship("CommunityPost", lazy="joined")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    @property
    def community(self):
        import forum.community as community
        return community.Community.by_id(self.community_id)

    def __repr__(self):
        return f"<CommunityComment(id={self.id}, comment_id={self.comment_id}, community_id={self.community_id})>"

