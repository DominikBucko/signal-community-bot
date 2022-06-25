import logging
import threading
import json
import os
from commands import *
import db.models as database
import db.database_functions as db
import signalbot.bot_utils as bot_utils
from signalbot import SignalBot
from db.commands.migrate_db import migrate_db
from db.commands.fill_db import fill_db
from commands.timed_commands import init_gaming_poll
from config import config

logging.getLogger().setLevel(logging.INFO)
logging.getLogger("apscheduler").setLevel(logging.WARNING)


def main():
    migrate_db()
    fill_db()

    bot = SignalBot(config)

    database.database.init(database=os.environ['DB_NAME'],
                           host=os.environ["DB_HOST"],
                           user=os.environ["DB_USER"],
                           password=os.environ["DB_PASSWORD"],
                           port=os.environ["DB_PORT"])

    bot.register(StaticCommands())
    bot.register(FunctionalCommands())

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
    #
    # bot_thread = threading.Thread(target=init_gaming_poll,
    #                               args=(bot, bot.storage["registered_chats"]["bot test group"]["optional_id"]))
    # bot_thread.start()
    bot.start()


if __name__ == "__main__":
    main()


# TODO make interactive TODO list
# TODO check if shelve satisfies our needs or we need some database