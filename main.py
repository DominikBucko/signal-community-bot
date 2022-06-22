import logging
import threading
import json
from commands import *
from commands.admin_commands.add_new_contact import AddContactCommand
from signalbot import SignalBot
from commands.gaming_poll_timed import init_gaming_poll
from config import config

logging.getLogger().setLevel(logging.INFO)
logging.getLogger("apscheduler").setLevel(logging.WARNING)


def main():

    admins_dict = {}
    with open("admins.json") as admins_json:
        admins_dict = json.load(admins_json)

    bot = SignalBot(config, admins_dict)

    bot.register(GamingPollCommand())
    bot.register(VypicujVilaCommand())
    bot.register(SendImageCommand())
    bot.register(AddContactCommand())

    for c in bot.storage["registered_chats"].values():
        try:
            bot.listen(**c)
        except Exception as e:
            print(e, c)

    bot_thread = threading.Thread(target=init_gaming_poll,
                                  args=(bot, bot.storage["registered_chats"]["bot test group"]["optional_id"]))
    bot_thread.start()
    bot.start()


if __name__ == "__main__":
    main()


# TODO make interactive TODO list
# TODO check if shelve satisfies our needs or we need some database