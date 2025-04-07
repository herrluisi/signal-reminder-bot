from signalbot import Command, Context
from imports.db.reminder import add_reminder


class ReminderCommand(Command):
    def describe(self) -> str:
        return "🏓 Ping Command: Listen for a ping"

    async def handle(self, c: Context):
        print(c.message.__dict__)
        if c.message.text:
            command = c.message.text.lower()

            if command == "remindme":
                message = await c.send("I will remind you")
                print(message)
                print(message.text)
                return

        if c.message.reaction:
            emoji = c.message.reaction
            print(emoji)
