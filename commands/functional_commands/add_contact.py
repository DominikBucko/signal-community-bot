from commands.utils import is_super_admin
import db.database_functions as db
from signalbot import Context
import peewee as pw

async def execute_add_user_to_listeners(c: Context):
    try:
        command = c.message.text
        source = db.get_user(c.message.source)

        phone_number = command.split()[-1]
        name = " ".join(command.split()[1:-1])

        db.add_chat(name=name, required_id=phone_number)
        c.bot.user_chats.add(phone_number)

        await c.react("✅")
        await send_welcome_message_user(c.bot, phone_number, source.name)

    # todo, create a proper error role based mechanism
    # if user is not in database as admin, temporary solution
    except pw.DoesNotExist:
        await c.react("👮")

    except Exception as e:
        await c.react("❌")
        print(e)
        raise e


async def send_welcome_message_user(bot, number, admin_name):
    receiver = number
    message = f"Hello! I'm your friendly neighbourhood Bot Will-E (sent by your friend {admin_name}), ready to serve " \
              f"you. I listen to your commands and will try to respond appropriately. You can type 'list commands' to" \
              f" see what I can do. Nice meeting you!"
    await bot.send(receiver=receiver, text=message, listen=False)
