from commands.utils import is_super_admin
import db.database_functions as db
from signalbot import Context
import peewee as pw
import base64


async def execute_add_command(c: Context):
    command = c.message.text.split()

    try:
        name = command[1]
        description = " ".join(command[2:]) if len(command) > 2 else None
        db.add_command(name=name, description=description)
        await c.react("✅")

        if description is None:
            timestamp = await c.send("description ?")
            db.add_sent_message(signal_key=timestamp, description="description", command=name)

        timestamp = await c.send("text ?")
        db.add_sent_message(signal_key=timestamp, description="command", command=name)

        timestamp = await c.send("attachment ?")
        db.add_sent_message(signal_key=timestamp, description="attachment", command=name)

        for class_command in c.bot.commands:
            class_command.update_triggers()

    except Exception as e:
        await c.react("❌")
        raise e


async def update_command(c: Context):
    try:
        message_text = c.message.text
        quote = c.message.quote

        sent_message_object = db.get_sent_message(quote['id'])
        command = db.get_command_by_name(sent_message_object.command)

        if sent_message_object.description == "description":
            command.description = message_text
            command.save()

        elif sent_message_object.description == "command":
            command.command = message_text
            command.save()

        elif sent_message_object.description == "attachment":
            attachment = await c.bot.get_attachment(c.message.base64_attachments[0]['id'])
            command.attachment = attachment
            command.save()

        await c.react("✅")

    except Exception as e:
        raise e


async def change_command(c: Context):
    command = c.message.text.split()

    try:
        name = command[1]
        command = db.get_command_by_name(name=name)

        timestamp = await c.send("description ?")
        db.add_sent_message(signal_key=timestamp, description="description", command=command.name)

        timestamp = await c.send("text ?")
        db.add_sent_message(signal_key=timestamp, description="command", command=command.name)

        timestamp = await c.send("attachment ?")
        db.add_sent_message(signal_key=timestamp, description="attachment", command=command.name)


    except Exception as e:
        await c.react("❌")
        raise e
