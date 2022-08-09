from peewee import Model, Database, CharField, IntegerField, DateTimeField, \
    BooleanField, ForeignKeyField, TextField, FloatField, ManyToManyField, DatabaseProxy, PostgresqlDatabase
from playhouse.shortcuts import ThreadSafeDatabaseMetadata

database = PostgresqlDatabase(None)

class BaseModel(Model):
    class Meta:
        database = database
        model_metadata_class = ThreadSafeDatabaseMetadata


class User(BaseModel):
    name = CharField()
    required_id = CharField(primary_key=True)
    is_super_user = BooleanField(default=False)

# TODO create roles as enum field
class Roles(BaseModel):
    name = CharField(primary_key=True)


class Chats(BaseModel):
    name = CharField()
    required_id = CharField(primary_key=True)
    optional_id = CharField(null=True)


class UserChatRoles(BaseModel):
    user_id = ForeignKeyField(User, backref='user_chat_roles')
    chat_id = ForeignKeyField(Chats)
    role_id = ForeignKeyField(Roles)


class Command(BaseModel):
    command = CharField(null=True)
    name = CharField(primary_key=True)
    description = CharField(null=True)
    attachment = TextField(null=True)
    is_functional = BooleanField(default=False)
    # TODO roles required


class TimedCommands(Command):
    chat = ManyToManyField(Chats, backref='timed_commands')
    actuation_time = DateTimeField()
    repeat_every = IntegerField(null=True)
    repeat = BooleanField(default=False)
    server_time_offset = FloatField(default=-2)


class Todo(BaseModel):
    name = CharField()
    chat = ForeignKeyField(Chats, backref='todos')

    class Meta:
        depends_on = (Chats,)


class SentMessages(BaseModel):
    signal_key = CharField(primary_key=True)
    time_sent = DateTimeField()
    todo_id = ForeignKeyField(Todo, backref='sent_messages', on_delete='CASCADE')
    recipient = CharField()
    target_author = CharField()
