import os
import psycopg2
import db.models as db

from peewee import PostgresqlDatabase
from db.models import Chats, User, UserChatRoles, Roles, Command, TimedCommands, todo

from psycopg2 import extensions


conn = psycopg2.connect(host=os.environ["DB_HOST"],
                        user=os.environ["DB_USER"],
                        password=os.environ["DB_PASSWORD"],
                        port=os.environ["DB_PORT"]
                        )
conn.autocommit = True
conn.set_isolation_level(extensions.ISOLATION_LEVEL_AUTOCOMMIT)
try:
    with conn.cursor() as cursor:
        cursor.execute(f"SELECT datname FROM pg_database;")
        list_of_databases = cursor.fetchall()
        if (os.environ["DB_NAME"],) in list_of_databases:
            cursor.execute(f"DROP DATABASE {os.environ['DB_NAME']}")
        cursor.execute(f"CREATE DATABASE {os.environ['DB_NAME']}")
finally:
    if conn:
        conn.close()

db.database.init(database=os.environ['DB_NAME'],
                       host=os.environ["DB_HOST"],
                       user=os.environ["DB_USER"],
                       password=os.environ["DB_PASSWORD"],
                       port=os.environ["DB_PORT"])

db.database.create_tables([User, Roles, Chats, UserChatRoles, Command, TimedCommands, todo], safe=True)
