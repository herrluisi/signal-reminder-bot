import json
from os import getenv
from datetime import datetime, timedelta
from dotenv import load_dotenv

from sqlalchemy import Column, Integer, String, DateTime, Boolean
from .database import Base, session, engine

load_dotenv()


class Reminder(Base):
    __tablename__ = "reminders"
    id = Column(Integer, primary_key=True, autoincrement=True)
    date = Column(DateTime, nullable=False)
    message = Column(String, nullable=False)  # message to send
    number = Column(String, nullable=False, default=getenv("PHONE_NUMBER"))  # recipient number
    messageTimeStamp = Column(String)   # timestamp of the message which reminds the person for later use of "remine me again in 5 minutes as reaction"
    sent = Column(Boolean, default=False)  # whether the reminder has been sent or not

Base.metadata.create_all(bind=engine)


def load_reminders():
    """Load reminders from the database which aren't sent yet and are in the future."""
    print(datetime.now(), "load reminders after", datetime.now() - timedelta(minutes=1))
    reminders = session.query(Reminder).filter(
        Reminder.date > datetime.now() - timedelta(minutes=1)).order_by(Reminder.date).all()
    print(datetime.now(), "loaded reminders from db")
    return [
        {
            "id": reminder.id,
            "date": reminder.date.isoformat(),
            "message": reminder.message,
            "number": reminder.number,
            "sent": reminder.sent,
         } for reminder in reminders]


def add_reminder(date: datetime, message: str, number: str = getenv("PHONE_NUMBER")):
    """Add a new reminder to the database."""
    new_reminder = Reminder(date=date, message=message, number=number)
    session.add(new_reminder)
    session.commit()
    return new_reminder.id


def update_reminder(reminder_id: int, sent: bool):
    """Update the reminder status in the database."""
    reminder = session.query(Reminder).filter(Reminder.id == reminder_id).first()
    if reminder:
        reminder.sent = sent
        session.commit()
        return True
    return False


def repeat_reminder(reminder_id: int, duration: int):
    """Update the reminder date in the database.

    :param reminder_id: the id of the reminder
    :param duration: the duration of the repeated reminder in minutes
    :return:
    """
    reminder = session.query(Reminder).filter(Reminder.id == reminder_id).first()
    if reminder:
        new_reminder = Reminder(
            date=reminder.date + timedelta(minutes=duration),
            message=reminder.message,
            number=reminder.number,
        )
        session.add(new_reminder)
        session.commit()
        return True
    return False
