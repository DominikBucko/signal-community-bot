import commands.functional_commands as functional_commands
import db.database_functions as db
import logging

from signalbot import Command, Context, Message, MessageType


class FunctionalCommands(Command):
    def __init__(self):
        self.triggers = None
        self.update_triggers()

    def update_triggers(self):
        self.triggers = [command.name for command in db.get_functional_commands()]

    def describe(self) -> str:
        return "Functional commands triggered by text"

    async def handle(self, c: Context):
        message_text = c.message.text
        reaction = c.message.reaction

        if message_text and message_text.startswith(tuple(self.triggers)):
            if message_text == "list commands":
                await functional_commands.execute_list_commands(c)

            if message_text.startswith("!addcontact "):
                await functional_commands.execute_add_user_to_listeners(c)

            if message_text.startswith("!todo "):
                await functional_commands.add_item_to_todo(c)

            if message_text == "todo" or message_text == "Todo":
                await functional_commands.show_todo_list(c)

        if reaction and reaction['emoji'] == "👍":
            await functional_commands.delete_todo(c)
