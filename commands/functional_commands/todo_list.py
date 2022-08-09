import db.database_functions as db
from signalbot import Context
import peewee as pw

from signalbot.bot_utils import resolve_receiver


async def add_item_to_todo(c: Context):
    command = c.message.text
    recipient = c.message.recipient()
    item = " ".join(command.split()[1:])

    db.create_todo(name=item, chat_id=recipient)
    await c.react("✅")


async def show_todo_list(c: Context):
    todo_list = db.get_chat_todos(c.message.recipient())
    await c.send("Todo list:")
    for item in todo_list:
        timestamp = await c.send(item.name)
        db.add_sent_message(signal_key=timestamp,
                            todo_id=item.id,
                            recipient=resolve_receiver(c.bot.group_chats, c.message.recipient()),
                            target_author=c.bot.phone_number,
                            )


async def delete_todo(c: Context):
    reaction = c.message.reaction
    sent_message_object = db.get_sent_message(reaction['targetSentTimestamp'])

    params = (int(sent_message_object.signal_key),
              "✅",
              sent_message_object.recipient,
              sent_message_object.target_author)

    try:
        db.delete_todo(sent_message_object.todo_id)
        await c.bot.react_to_sent_message(*params)
    except Exception as e:
        raise e
