from signalbot import Command, Context


class ReminderCommand(Command):
    def describe(self) -> str:
        return "🏓 Ping Command: Listen for a ping"

    async def handle(self, c: Context):
        await c.start_typing()
        command = c.message.text.lower()
        emoji = c.message.text[0]

        if command == "remindme":
            await c.send("I will remind you")
            return