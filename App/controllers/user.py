from App.models import Reviewer, Admin
from App.database import db


def create_reviewer(username, password):
    newReviewer = Reviewer(username=username, password=password)
    db.session.add(newReviewer)
    db.session.commit()
    return newReviewer

def create_admin(username, password):
    newAdmin = Admin(username=username, password=password)
    db.session.add(newAdmin)
    db.session.commit()
    return newAdmin

#Leaving Admin out of the scope for now because I'm not sure what's the right way to do it
def get_user_by_username(username):
    user =  Reviewer.query.filter_by(username=username).first()
    return user

def get_user(id):
    return Reviewer.query.get(id)

def get_all_users():
    return Reviewer.query.all()

def get_all_users_json():
    users = Reviewer.query.all()
    if not users:
        return []
    users = [user.toJSON() for user in users]
    return users

def update_user(id, username):
    user = get_user(id)
    if user:
        user.username = username
        db.session.add(user)
        return db.session.commit()
    return None
