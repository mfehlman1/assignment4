"""
This file defines the database models
"""

import datetime
from .common import db, Field, auth
from pydal.validators import *


def get_user_email():
    return auth.current_user.get('email') if auth.current_user else None

def get_time():
    return datetime.datetime.utcnow()


db.define_table(
    'contact_card',
    Field("user_id", "reference auth_user"),
    Field('name', 'string', requires = IS_NOT_EMPTY()),
    Field('affiliation', 'string', requires= IS_NOT_EMPTY()),
    Field('description', 'text'),
    Field('image', 'upload'),
)

db.commit()
