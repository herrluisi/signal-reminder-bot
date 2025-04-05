from os import getenv
from dotenv import load_dotenv
from signalbot import SignalBot
from commands import (
    FridayCommand,
    PingCommand
)
import logging


logging.getLogger().setLevel(logging.INFO)
logging.getLogger("apscheduler").setLevel(logging.WARNING)

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

    # enable a chat command for all contacts and all groups
    # bot.register(PingCommand())
    # bot.register(ReplyCommand())

    # enable a chat command only for groups
    bot.register(PingCommand(), contacts=True, groups=True)

    # enable a chat command for one specific group with the name "My Group"
    bot.register(FridayCommand(), contacts=False, groups=["Reminders"])

    # chat command is enabled for all groups and one specific contact
    # bot.register(TriggeredCommand(), contacts=["+490123456789"], groups=True)
    #
    # bot.register(RegexTriggeredCommand())

    bot.start()


if __name__ == "__main__":
    main()
