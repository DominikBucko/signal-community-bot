import logging
from commands import *
import db.models as database
import db.database_functions as db
import signalbot.bot_utils as bot_utils
from signalbot import SignalBot
from db.fill_db import fill_db
from config import config

logging.getLogger().setLevel(logging.INFO)
logging.getLogger("apscheduler").setLevel(logging.WARNING)


def main():
    database.database.evolve(interactive=False, ignore_tables=['basemodel'])
    fill_db()

    bot = SignalBot(config)
    try:
        for chat in db.get_chats():
            if bot_utils.is_phone_number(chat.required_id):
                bot.user_chats.add(chat.required_id)
                continue

            if bot_utils.is_group_id(chat.optional_id) and bot_utils.is_internal_id(chat.required_id):
                bot.group_chats[chat.required_id] = chat.optional_id
                continue

            logging.warning(
                "[Bot] Can't listen for user/group because input does not look valid"
            )
    except Exception as e:
        logging.info("[Bot] Assigning chats failed", e)

    #
    # bot_thread = threading.Thread(target=init_gaming_poll,
    #                               args=(bot, bot.storage["registered_chats"]["bot test group"]["optional_id"]))
    # bot_thread.start()

    bot.register(StaticCommands())
    bot.register(FunctionalCommands())
    bot.start()


if __name__ == "__main__":
    main()
