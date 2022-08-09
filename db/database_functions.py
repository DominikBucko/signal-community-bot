import db.models as db
import datetime
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


### _TODO ###
def get_chat_todos(chat_id):
    return db.Todo.select().where(db.Todo.chat == chat_id)


def get_todo_by_name(chat_id, name):
    return db.Todo.get(db.Todo.chat == chat_id, db.Todo.name == name)


def create_todo(name, chat_id):
    todo = db.Todo.create(
        name=name,
        chat=chat_id
    )
    todo.save()


def delete_todo(todo_id):
    todo = db.Todo.get(db.Todo.id == todo_id)
    todo.delete_instance()
    todo.save()


def add_sent_message(signal_key, todo_id, recipient="", target_author=""):
    sent_message = db.SentMessages.create(
        signal_key=signal_key,
        todo_id=todo_id,
        time_sent=datetime.datetime.now(),
        recipient=recipient,
        target_author=target_author
    )
    sent_message.save()


def get_sent_message(signal_key):
    return db.SentMessages.get(db.SentMessages.signal_key == signal_key)
