from signalbot import Context
from signalbot.api import SignalAPI

from dotenv import load_dotenv
from os import getenv

load_dotenv()

api = SignalAPI(signal_service=getenv("SIGNAL_SERVICE"), phone_number=getenv("PHONE_NUMBER"))


async def send_message(text: str, recipient: str):
    """
    Send a message to the recipient.

    :param text: The text to send.
    :param recipient: The number of the recipient.
    """
    message = await api.send(recipient, text)
    return message
