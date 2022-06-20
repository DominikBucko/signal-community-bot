from signalbot import Command, Context


class VypicujVilaCommand(Command):
    def describe(self) -> str:
        return "Send William to the heaven"

    async def handle(self, c: Context):
        command = c.message.text

        if "vypicuj vila" in command.lower():
            await c.send(f"...")
            return