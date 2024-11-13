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
    Field('contact_name', 'string', requires = IS_NOT_EMPTY()),
    Field('contact_affiliation', 'string', requires= IS_NOT_EMPTY()),
    Field('contact_description', 'text'),
    Field('contact_image', 'upload'),
)

db.commit()
