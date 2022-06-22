import random

from signalbot import Command, Context

spravicky = ["VILO UZ DRZ PICU", "VILO KLUD", "VILO OMG UZ CICHO", "KURVA DO PICI VILO ACH", "...", "uz si picujte sami, ja uz nevladzem"]


class VypicujVilaCommand(Command):
    def describe(self) -> str:
        return "Send William to the heaven"

    async def handle(self, c: Context):
        command = c.message.text

        if command and "vypicuj vila" in command.lower():
            await c.send(random.choice(spravicky))
            return