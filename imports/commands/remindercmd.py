from datetime import datetime, timedelta
import json

from signalbot import Command, Context


from imports.db.reminder import add_reminder


class ReminderCommand(Command):
    def describe(self) -> str:
        return "🏓 Ping Command: Listen for a ping"

    async def handle(self, c: Context):
        if c.message.text:
            # tries if the message is a number
            try:
                minutes = float(c.message.text)
                reminder_text = json.loads(c.message.raw_message).get("envelope").get("syncMessage").get("sentMessage").get("quote").get("text")
                add_reminder(datetime.now() + timedelta(minutes=minutes), reminder_text)

            except:
                command = c.message.text.split(" ")[0].lower()

                if command == "remindme":
                    message = c.message.text
                    # Example: remindme 30 There's a meeting in 5 Minutes!
                    time = float(message.split(" ")[1])
                    reminder = ""
                    for word in message.split(" ")[2:]:
                        if word.startswith("+49"):
                            number = word
                            break
                        reminder += word + " "
                    if message.count("+49") > 0:
                        add_reminder(datetime.now() + timedelta(minutes=time), reminder, number)
                        await c.send(
                            f"I will remind {number} in {time} minutes ({datetime.now() + timedelta(minutes=time)}:\n{reminder})")
                        return
                    add_reminder(datetime.now() + timedelta(minutes=time), reminder)
                    await c.send(f"I will remind you in {time} minutes ({datetime.now() + timedelta(minutes=time)}:\n{reminder})")
