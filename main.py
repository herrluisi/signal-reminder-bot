from os import getenv
from dotenv import load_dotenv
from signalbot import SignalBot
from commands import (
    FridayCommand,
    PingCommand, ReminderCommand
)
import logging


logging.getLogger().setLevel(logging.INFO)
# logging.getLogger("apscheduler").setLevel(logging.CRITICAL)

load_dotenv()


def main():
    signal_service = getenv("SIGNAL_SERVICE")
    phone_number = getenv("PHONE_NUMBER")

    config = {
        "signal_service": signal_service,
        "phone_number": phone_number,
        "storage": None,
    }
    bot = SignalBot(config)

    # enable a chat command for one specific group with the name "My Group"
    bot.register(FridayCommand(), contacts=False, groups=["Reminders"])
    bot.register(PingCommand(), contacts=False, groups=["Reminders"])
    bot.register(ReminderCommand(), contacts=False, groups=["Reminders"])

    bot.start()


if __name__ == "__main__":
    main()
