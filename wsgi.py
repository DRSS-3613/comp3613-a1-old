import click, pytest, sys
from flask import Flask
from flask.cli import with_appcontext, AppGroup

from App.database import create_db, get_migrate
from App.main import create_app
from App.controllers import (
    create_user,
    get_all_users_json,
    get_all_users,
    create_student,
    get_all_students_json,
    create_review,
    get_reviews_by_student_id,
    upvote_review,
    downvote_review,
)

# This commands file allow you to create convenient CLI commands for testing controllers

app = create_app()
migrate = get_migrate(app)

# This command creates and initializes the database
@app.cli.command("init", help="Creates and initializes the database")
def initialize():
    create_db(app)
    print("database intialized")


"""
User Commands
"""

# Commands can be organized using groups

# create a group, it would be the first argument of the command
# eg : flask user <command>
user_cli = AppGroup("user", help="User object commands")

# Then define the command and any parameters and annotate it with the group (@)
@user_cli.command("create", help="Creates a user")
@click.argument("username", default="rob")
@click.argument("password", default="robpass")
def create_user_command(username, password):
    create_user(username, password)
    print(f"{username} created!")


# this command will be : flask user create bob bobpass


@user_cli.command("list", help="Lists users in the database")
@click.argument("format", default="string")
def list_user_command(format):
    if format == "string":
        print(get_all_users())
    else:
        print(get_all_users_json())


app.cli.add_command(user_cli)  # add the group to the cli


"""
Generic Commands
"""


@app.cli.command("init")
def initialize():
    create_db(app)
    print("database intialized")


"""
Test Commands
"""

test = AppGroup("test", help="Testing commands")


@test.command("user", help="Run User tests")
@click.argument("type", default="all")
def user_tests_command(type):
    if type == "unit":
        sys.exit(pytest.main(["-k", "UserUnitTests"]))
    elif type == "int":
        sys.exit(pytest.main(["-k", "UserIntegrationTests"]))
    else:
        sys.exit(pytest.main(["-k", "App"]))


app.cli.add_command(test)

student_cli = AppGroup("student", help="Student object commands")


@student_cli.command("create-student")
@click.argument("name")
def create_student_command(name):
    create_student(name)
    print(f"{name} created!")


@student_cli.command("get-students")
def get_students_command():
    print(get_all_students_json())


app.cli.add_command(student_cli)


review_cli = AppGroup("review", help="Review object commands")


@review_cli.command("create-review")
@click.argument("student_id")
@click.argument("text")
def create_review_command(student_id, text):
    create_review(student_id, text)
    print(f"Review created!")


@review_cli.command("get-reviews")
@click.argument("student_id")
def get_reviews_by_student_id_command(student_id):
    print(get_reviews_by_student_id(student_id))


@review_cli.command("upvote-review")
@click.argument("review_id")
def upvote_review_command(review_id):
    upvote_review(review_id)


@review_cli.command("downvote-review")
@click.argument("review_id")
def downvote_review_command(review_id):
    downvote_review(review_id)


app.cli.add_command(review_cli)
