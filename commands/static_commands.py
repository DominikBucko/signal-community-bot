import random
import db.database_functions as db

from signalbot import Command, Context


class StaticCommands(Command):
    def __init__(self):
        self.triggers = None
        self.update_triggers()

    def update_triggers(self):
        self.triggers = [command.name for command in db.get_nonfunctional_commands()]

    def describe(self) -> str:
        return "Commands triggered by text"

    async def handle(self, c: Context):
        message_text = c.message.text

        if message_text and message_text.lower() in self.triggers:
            command = db.get_command_by_name(message_text.lower())
            response_text = command.command if not None else ""
            attachment = command.attachment if not None else ""
            if attachment:
                await c.send(response_text,
                             base64_attachments=[attachment],
                             )
            else:
                await c.send(response_text)