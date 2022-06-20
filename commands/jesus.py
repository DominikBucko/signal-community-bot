import random

from signalbot import Command, Context
from .images import ukaz_picu, jesus, scare_me


class SendImageCommand(Command):
    def describe(self) -> str:
        return ""

    async def handle(self, c: Context):
        command = c.message.text

        if command.lower() == "scare me":
            image = scare_me.scare_me
            await c.send("",
                         base64_attachments=[image],
                         )
            return

        if command.lower() == "ukaz picu":
            image = ukaz_picu.ukaz_picu
            await c.send("",
                         base64_attachments=[image],
                         )
            return

        if command.lower() == "jesus":
            image = jesus.jesus
            await c.send("",
                         base64_attachments=[image],
                         )
            return