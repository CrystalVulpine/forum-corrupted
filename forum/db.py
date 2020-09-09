from sqlalchemy import *

from forum.user import *
from forum.community import *
from forum.relationships import *

def init(db):
    db.create_all()
    db.session.commit()

