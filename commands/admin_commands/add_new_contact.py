from signalbot import Command, Context
from misc.helper_functions import register_contact_in_storage, send_welcome_message_user, get_admin_name


class AddContactCommand(Command):
    def describe(self) -> str:
        return "Adding new contact for bot to listen to. Example: '!addcontact Jozo Mrkva +421949186020'"

    async def handle(self, c: Context):
        command = c.message.text
        sender = c.message.source

        if command.startswith("!addcontact ") and sender in c.bot.admins.values():
            phone_number = command.split()[-1]
            name = " ".join(command.split()[1:-1])
            register_contact_in_storage(c.bot, name, phone_number)
            await c.send(f"{name} successfully registered.")
            await send_welcome_message_user(c.bot, phone_number, get_admin_name(c.bot, sender))
            return
