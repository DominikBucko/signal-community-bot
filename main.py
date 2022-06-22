import logging
import threading

from commands import *
from signalbot import SignalBot
from commands.gaming_poll_timed import init_gaming_poll

logging.getLogger().setLevel(logging.INFO)
logging.getLogger("apscheduler").setLevel(logging.WARNING)

existing_contacts = {
    "Dominik": {"required_id": "+421949186020"},
    "Janko": {"required_id": "+421950764723"},
    "Petrik": {"required_id": "+421903306221"},
    "bot test group": {"required_id": "group.VHBSZVBSdytDaDNZZkRsQ2N6bVluQnR3Yld1QUpDVkxyVXB2bDdGajNnYz0=",
                       "optional_id": "TpRePRw+Ch3YfDlCczmYnBtwbWuAJCVLrUpvl7Fj3gc="},
    "left4ded": {"required_id": "group.dGMxREp4di80U3l2c0ZiQUIraitTTUordmljWk9QL3luc2N2OGZ2UW1Zbz0=",
                 "optional_id": "tc1DJxv/4SyvsFbAB+j+SMJ+vicZOP/ynscv8fvQmYo="},
}


def main():
    signal_service = "127.0.0.1:8080"
    phone_number = "+421951731737"

    config = {
        "signal_service": signal_service,
        "phone_number": phone_number,
        "storage": {
            "redis_host": "127.0.0.1",
            "redis_port": 6379,
            "redis_password": "eYVX7EwVmmxKPCDmwMtyKVge8oLd2t81",
        }
    }
    bot = SignalBot(config)

    bot.register(GamingPollCommand())
    bot.register(VypicujVilaCommand())
    bot.register(SendImageCommand())

    for contact, c in existing_contacts.items():
        try:
            bot.listen(**c)
        except Exception as e:
            print(e, contact, c)

    bot_thread = threading.Thread(target=init_gaming_poll,
                                  args=(bot, existing_contacts["bot test group"]["optional_id"]))
    bot_thread.start()
    bot.start()

if __name__ == "__main__":
    main()