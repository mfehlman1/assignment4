"""
This file defines actions, i.e. functions the URLs are mapped into
The @action(path) decorator exposed the function at URL:

    http://127.0.0.1:8000/{app_name}/{path}

If app_name == '_default' then simply

    http://127.0.0.1:8000/{path}

If path == 'index' it can be omitted:

    http://127.0.0.1:8000/

The path follows the bottlepy syntax.

@action.uses('generic.html')  indicates that the action uses the generic.html template
@action.uses(session)         indicates that the action uses the session
@action.uses(db)              indicates that the action uses the db
@action.uses(T)               indicates that the action uses the i18n & pluralization
@action.uses(auth.user)       indicates that the action requires a logged in user
@action.uses(auth)            indicates that the action requires the auth object

session, db, T, auth, and tempates are examples of Fixtures.
Warning: Fixtures MUST be declared with @action.uses({fixtures}) else your app will result in undefined behavior
"""

from py4web import action, request, abort, redirect, URL
from yatl.helpers import A
from .common import db, session, T, cache, auth, logger, authenticated, unauthenticated, flash
from .models import get_user_email


@action('index')
@action.uses('index.html', db, auth.user)
def index():
    return dict(
        get_contacts_url = URL('get_contacts'),
        add_contact_url = URL('add_contact'),
        update_contact_url = URL('update_contact'),
        delete_contact_url = URL('delete_contact'),
        upload_photo_url = URL('upload_photo')
        # Complete. 
    )

@action('get_contacts')
@action.uses(db, auth.user)
def get_contacts():
    user_email = get_user_email()
    contacts = db(db.contact_card.user_email == user_email).select().as_list() # Complete. 
    return dict(contacts=contacts)

# You can add more methods. 

@action('add_contact', method = "POST")
@action.uses(db, auth.user)
def add_contact():
    user_email = get_user_email()
    contact_id = db.contact_card.insert(
        user_email = user_email,
        contact_name = request.json.get("name", ""),
        contact_affiliation = request.json.get("affiliation", ""),
        contact_description = request.json.get("description", ""),
        contact_image = "https://bulma.io/assets/images/placeholders/96x96.png"
    )
    return dict(contact_id = contact_id)

@action('update_contact/<contact_id:int>', method = "PUT")
@action.uses(db, auth.user)
def update_contact(contact_id): 
    user_email = get_user_email()
    contact = db((db.contact_card.id == contact_id) & (db.contact_card.user_email == user_email)).select().first()
    if not contact:
        abort(403)
    contact.update_record(
        contact_name = request.json.get("name", contact.contact_name),
        contact_affiliation = request.json.get("affiliation", contact.contact_affiliation),
        contact_description = request.json.get("description", contact.contact_description)
    )
    return dict(status = "success")

@action('delete_contact/<contact_id:int>', method = "DELETE")
@action.uses(db, auth.user)
def delete_contact(contact_id):
    user_email = get_user_email()
    contact = db((db.contact_card.id == contact_id) & (db.contact_card.user_email == user_email)).select().first()
    if not contact:
        abort(403)
    contact.delete_record()
    return dict(status = "deleted")

@action('upload_photo/<contact_id:int>', method = "POST")
@action.uses(db, auth.user)
def upload_photo(contact_id):
    user_email = get_user_email()
    contact = db((db.contact_card.id == contact_id) & (db.contact_card.user_email == user_email)).select().first()
    if not contact:
        abort(403)
    uploaded_photo = request.files.get("photo")
    if uploaded_photo:
        photo_url = db.contact_card.contact_image.store(uploaded_photo, uploaded_photo.filename)
        contact.update_record(contact_image=photo_url)
        return dict(photo_url=URL('static', photo_url))
    return dict(error = "photo not uploaded")
