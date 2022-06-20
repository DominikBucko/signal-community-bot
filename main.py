import os
import logging

from commands import GamingPollCommand, VypicujVilaCommand
from signalbot import SignalBot

import asyncio

logging.getLogger().setLevel(logging.INFO)
logging.getLogger("apscheduler").setLevel(logging.WARNING)

# async def schedule():
#     from datetime import date
#     import time
#     print(date.today())
#     time.sleep(10)

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
    # internal_id = os.environ["GROUP_INTERNAL_ID"]
    #
    config = {
        "signal_service": signal_service,
        "phone_number": phone_number,
        "storage": None,
    }
    bot = SignalBot(config)

    bot.register(GamingPollCommand())
    bot.register(VypicujVilaCommand())

    for contact, c in existing_contacts.items():
        try:
            bot.listen(**c)
        except Exception as e:
            print(e, contact, c)

    bot.start()


if __name__ == "__main__":
    main()
