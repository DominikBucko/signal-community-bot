from signalbot import Command, Context


class GamingPollCommand(Command):
    def describe(self) -> str:
        return "Lets vote for gaming night"

    async def handle(self, c: Context):
        command = c.message.text

        if command.lower() == "no so":
            await c.send("NO CO KOKOCI, DAVAJTE REACTY TAKOJ!!!!\n"
                         f"❤ - Yes\n"
                         f"👎 - No\n"
                         f"👍 - Yes, ked ostatni pojdu\n"
                         f"😥 - Mozem jebac\n"
                         f"😮 - Neskor sa napojim"
                         )
            return
