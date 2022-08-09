import asyncio
import time
import shelve
import logging

from apscheduler.schedulers.asyncio import AsyncIOScheduler

from .api import SignalAPI, ReceiveMessagesError
from .command import Command
from .message import Message, UnknownMessageFormatError, MessageType
from .context import Context
from .bot_utils import is_group_id, is_internal_id, is_phone_number, \
    should_react, SignalBotError, resolve_receiver


class SignalBot:
    def __init__(self, config: dict):
        """SignalBot

        Example Config:
        ===============
        signal_service: "127.0.0.1:8080"
        phone_number: "+49123456789"
        """
        self.config = config

        self.commands = []  # populated by .register()
        self.user_chats = set()
        self.group_chats = {}

        # Required
        self._init_api()
        self._init_event_loop()
        self._init_scheduler()

    def _init_api(self):
        try:
            self.phone_number = self.config["phone_number"]
            self.signal_service = self.config["signal_service"]
            self._signal = SignalAPI(self.signal_service, self.phone_number)
        except KeyError:
            raise SignalBotError("Could not initialize SignalAPI with given config")

    def _init_event_loop(self):
        self._event_loop = asyncio.get_event_loop()
        self._q = asyncio.Queue()

    def _init_scheduler(self):
        try:
            self.scheduler = AsyncIOScheduler(event_loop=self._event_loop)
        except Exception as e:
            raise SignalBotError(f"Could not initialize scheduler: {e}")

    def register(self, command: Command):
        command.bot = self
        command.setup()
        self.commands.append(command)

    def start(self):
        self._event_loop.create_task(self._produce_consume_messages())

        # Add more scheduler tasks here
        # self.scheduler.add_job(...)
        self.scheduler.start()

        # Run event loop
        self._event_loop.run_forever()

    async def send(
            self,
            receiver: str,
            text: str,
            base64_attachments: list = None,
            listen: bool = False,
    ) -> int:
        resolved_receiver = resolve_receiver(self.group_chats, receiver)
        resp = await self._signal.send(
            resolved_receiver, text, base64_attachments=base64_attachments
        )
        resp_payload = await resp.json()
        timestamp = resp_payload["timestamp"]
        logging.info(f"[Bot] New message {timestamp} sent:\n{text}")

        if listen:
            if is_phone_number(receiver):
                sent_message = Message(
                    source=receiver,  # otherwise we can't respond in the right chat
                    timestamp=timestamp,
                    type=MessageType.SYNC_MESSAGE,
                    text=text,
                    base64_attachments=base64_attachments,
                    group=None,
                )
            else:
                sent_message = Message(
                    source=self.phone_number,  # no need to pretend
                    timestamp=timestamp,
                    type=MessageType.SYNC_MESSAGE,
                    text=text,
                    base64_attachments=base64_attachments,
                    group=receiver,
                )
            await self._ask_commands_to_handle(sent_message)

        return timestamp

    async def react(self, message: Message, emoji: str):
        # TODO: check that emoji is really an emoji
        recipient = resolve_receiver(self.group_chats, message.recipient())
        target_author = message.source
        timestamp = message.timestamp
        await self._signal.react(recipient, emoji, target_author, timestamp)
        logging.info(f"[Bot] New reaction: {emoji}")

    async def react_to_sent_message(self, timestamp, emoji, recipient, target_author):
        await self._signal.react(recipient, emoji, target_author, timestamp)
        logging.info(f"[Bot] New reaction: {emoji}")

    async def start_typing(self, receiver: str):
        receiver = resolve_receiver(self.group_chats, receiver)
        await self._signal.start_typing(receiver)

    async def stop_typing(self, receiver: str):
        receiver = resolve_receiver(self.group_chats, receiver)
        await self._signal.stop_typing(receiver)

    async def _produce_consume_messages(self, producers=1, consumers=3) -> None:
        producers = [
            asyncio.create_task(self._produce(n)) for n in range(1, producers + 1)
        ]
        consumers = [
            asyncio.create_task(self._consume(n)) for n in range(1, consumers + 1)
        ]
        await asyncio.gather(*producers)
        await self._q.join()
        for c in consumers:
            c.cancel()

    async def _produce(self, name: int) -> None:
        logging.info(f"[Bot] Producer #{name} started")
        try:
            async for raw_message in self._signal.receive():
                logging.info(f"[Raw Message] {raw_message}")

                try:
                    message = Message.parse(raw_message)
                    if not should_react(self.user_chats, self.group_chats, message):
                        continue
                    await self._ask_commands_to_handle(message)

                except UnknownMessageFormatError:
                    logging.info(f"[Bot] Unknown message format: {raw_message}")

        except ReceiveMessagesError as e:
            # TODO: retry strategy
            raise SignalBotError(f"Cannot receive messages: {e}")

    async def _ask_commands_to_handle(self, message: Message):
        for command in self.commands:
            await self._q.put((command, message, time.perf_counter()))

    async def _consume(self, name: int) -> None:
        logging.info(f"[Bot] Consumer #{name} started")
        while True:
            try:
                await self._consume_new_item(name)
            except Exception:
                continue

    async def _consume_new_item(self, name: int) -> None:
        command, message, t = await self._q.get()
        now = time.perf_counter()
        logging.info(f"[Bot] Consumer #{name} got new job in {now - t:0.5f} seconds")

        # handle Command
        try:
            context = Context(self, message)
            await command.handle(context)
        except Exception as e:
            logging.error(f"[{command.__class__.__name__}] Error: {e}")
            raise e

        # done
        self._q.task_done()
