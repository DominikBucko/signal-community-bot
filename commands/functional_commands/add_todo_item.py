import db.database_functions as db
from signalbot import Context
import peewee as pw


async def add_item_to_todo(c: Context):
    command = c.message.text
    item = " ".join(command.split()[1:])
