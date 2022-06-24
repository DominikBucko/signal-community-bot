import db.database_functions as db
from signalbot import Command, Context

async def execute_list_commands(c: Context):
    # Non-functional commands
    response = "Static commands:\n"
    for command in db.get_nonfunctional_commands():
        response += f"{command.name} - {command.description}\n"
    # Functional commands
    response += "\nFunctional commands:\n"
    for command in db.get_functional_commands():
        response += f"{command.name} - {command.description}\n"

    await c.send(response)