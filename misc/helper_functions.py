import asyncio
import aiohttp
import logging
from signalbot.bot_utils import resolve_receiver


def register_contact_in_storage(bot, name, phone_number):
    bot.storage["registered_chats"][name] = {"required_id": phone_number}
    bot.storage.sync()
    bot.listen(**bot.storage["registered_chats"][name])


# run with asyncio.run(get_group_registration_dict)
async def get_group_registration_dict(bot, optional_id):
    signal_service = bot.config["signal_service"]
    phone_number = bot.config["phone_number"]
    async with aiohttp.ClientSession() as session:
        async with session.get(f"http://{signal_service}/v1/groups/{phone_number}") as resp:
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
