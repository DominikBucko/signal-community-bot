import asyncio
import aiohttp
import logging
from signalbot.bot_utils import resolve_receiver
from signalbot import Command, Context
import functools


# run with asyncio.run(get_group_registration_dict)
async def get_group_registration_dict(bot, optional_id):
    async with aiohttp.ClientSession() as session:
        async with session.get(f"http://{bot.signal_service}/v1/groups/{bot.phone_number}") as resp:
            if resp.status == 200:
                response_body = await resp.json()
                for group in response_body:
                    if group["internal_id"] == optional_id:
                        return group["id"]

            else:
                logging.info("Signal service failed to fetch group info")
                raise Exception

    logging.info("Group optional id was not found. This should never happen !")
    raise Exception


async def send_welcome_message_user(bot, number, admin_name):
    receiver = resolve_receiver(bot.group_chats, number)
    message = f"Hello! I'm your friendly neighbourhood Bot Will-E (sent by your friend {admin_name}), ready to serve " \
              f"you. I listen to your commands and will try to respond appropriately. You can type 'list commands' to" \
              f" see what I can do. Nice meeting you!"
    await bot.send(receiver=receiver, text=message, listen=False)


async def send_async_message_to(bot, receiver, text):
    asyncio.run(bot.send(receiver=receiver, text=text, listen=False))


def get_admin_name(bot, admin_number):
    for name, number in bot.admins.items():
        if number == admin_number:
            return name


async def mention_required(func):
    # @functools.wraps(func)
    async def wrapper(*args, **kwargs):
        context: Context
        try:
            context = args[1]
        except IndexError:
            context = None

        if context is None:
            return
        if context.bot.phone_number in context.message.mentions:
            await func(*args, **kwargs)

        return
    return wrapper
