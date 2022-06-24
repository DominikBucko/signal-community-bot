import asyncio
import logging

from signalbot import SignalBot
import time
from datetime import datetime

gaming_poll_message = f"TIMED NO CO KOKOCI, DAVAJTE REACTY TAKOJ!!!!\n" \
                      f"❤ - Yes\n" \
                      f"👎 - No\n" \
                      f"👍 - Yes, ked ostatni pojdu\n" \
                      f"😥 - Mozem jebac\n" \
                      f"😮 - Neskor sa napojim"


def init_gaming_poll(bot: SignalBot, gaming_channel_key: str):
    logging.info("[GAMING POOL SCHEDULER] started")
    while True:
        time_now = datetime.now()
        if time_now.hour == 19 and time_now.minute == 30:
            asyncio.run(bot.send(receiver=gaming_channel_key, text=gaming_poll_message, listen=False))
        time.sleep(60)
