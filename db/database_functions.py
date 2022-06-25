import db.models as db
import db.models as models
from multimethods import multimethod


### USERS ###
@db.database.atomic()
def add_user(name, phone_number, is_super_user=False):
    user = db.User.create(
        name=name,
        required_id=phone_number,
        is_super_user=is_super_user
    )
    user.save()


def get_user(phone_number):
    return db.User.get(db.User.required_id == phone_number)


### CHATS ###
@db.database.atomic()
def add_chat(name, required_id, optional_id=None):
    chat = db.Chats.create(
        name=name,
        required_id=required_id,
        optional_id=optional_id
    )
    chat.save()


def get_chats():
    return db.Chats.select()


### COMMANDS ###
@db.database.atomic()
def add_command(name, command=None, description=None, attachment=None, is_functional=False):
    command = command.lower() if command else None
    command = db.Command.create(
        name=name,
        command=command,
        description=description,
        attachment=attachment,
        is_functional=is_functional
    )
    command.save()


def get_nonfunctional_commands():
    return db.Command.select().where(db.Command.is_functional == False)


def get_functional_commands():
    return db.Command.select().where(db.Command.is_functional == True)


def get_command_by_name(name):
    return db.Command.get(db.Command.name == name)
