from App.models import Reviewer, Admin
from App.database import db


# reviewer functions
def create_reviewer(username, password):
    new_reviewer = Reviewer(username=username, password=password)
    db.session.add(new_reviewer)
    db.session.commit()
    return new_reviewer


def get_reviewer_by_id(id):
    return Reviewer.query.get(id)


def get_reviewer_by_username(username):
    return Reviewer.query.filter_by(username=username).first()


def get_all_reviewers():
    return Reviewer.query.all()


def get_all_reviewers_json():
    reviewers = Reviewer.query.all()
    if not reviewers:
        return []
    reviewers = [reviewer.to_json() for reviewer in reviewers]
    return reviewers


def update_reviewer(id, username):
    reviewer = get_reviewer_by_id(id)
    if reviewer:
        reviewer.username = username
        db.session.add(reviewer)
        return db.session.commit()
    return None


# admin functions
def create_admin(username, password):
    new_admin = Admin(username=username, password=password)
    db.session.add(new_admin)
    db.session.commit()
    return new_admin


def get_admin_by_id(id):
    return Admin.query.get(id)


def get_admin_by_username(username):
    return Admin.query.filter_by(username=username).first()


def get_all_admins():
    return Admin.query.all()


def get_all_admins_json():
    admins = Admin.query.all()
    if not admins:
        return []
    admins = [admin.to_json() for admin in admins]
    return admins


def update_admin(id, username):
    admin = get_admin_by_id(id)
    if admin:
        admin.username = username
        db.session.add(admin)
        return db.session.commit()
    return None


# all users
def get_all_users():
    return Reviewer.query.all() + Admin.query.all()


def get_all_users_json():
    users = get_all_users()
    if not users:
        return []
    users = [user.toJSON() for user in users]
    return users
