import random
import time
from os import getenv
from dotenv import load_dotenv
import threading
import asyncio
import nest_asyncio

from datetime import datetime, timedelta

from signalbot import SignalBot
from imports.commands import (
    ReminderCommand
)
import logging

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from imports.db.reminder import load_reminders, add_reminder, Reminder
from imports.db.database import session

nest_asyncio.apply()


logging.getLogger().setLevel(logging.INFO)

load_dotenv()


async def send_reminder(id, message, number):
    print(f"{datetime.now()} Sending reminder to {number}: {message}")
    session.query(Reminder).filter(Reminder.id == id).update({"sent": True})


async def run_scheduler():
    """
    schedules the reminders
    """
    scheduler = AsyncIOScheduler(timezone=getenv("TIMEZONE"))  # IMPORTANT: Set your timezone
    scheduler.start()

    # Periodic check loop
    while True:
        print(f"[{datetime.now()}] Periodic check for new/updated reminders...")

        # load reminders from database
        reminders_from_storage = load_reminders()
        print(f"loaded {len(reminders_from_storage)} from db")
        scheduled_job_ids = {job.id for job in scheduler.get_jobs()}
        loaded_reminder_ids = {f"reminder_{r['id']}" for r in reminders_from_storage}

        # Schedule new or updated reminders
        for reminder in reminders_from_storage:
            job_id = f"reminder_{reminder['id']}"
            run_time = datetime.fromisoformat(reminder.get('date'))

            # Check if job needs to be added or updated
            existing_job = scheduler.get_job(job_id)
            needs_scheduling = False
            if not existing_job and run_time > datetime.now(run_time.tzinfo):  # Only schedule future jobs
                needs_scheduling = True
                print(f"  - New reminder found: {job_id}")

            if needs_scheduling:
                scheduler.add_job(send_reminder, 'date', run_date=run_time,
                                  args=[reminder.get("id"), reminder.get("message"), reminder.get("number")],
                                  id=job_id, replace_existing=True)  # Replace handles adding/updating
                print(f"  - Scheduled/Updated job {job_id} for {run_time}")

        # Remove jobs for reminders that no longer exist or are marked sent
        jobs_to_remove = scheduled_job_ids - loaded_reminder_ids
        for job_id in jobs_to_remove:
            # Ensure to only remove reminder jobs
            if job_id.startswith("reminder_"):
                scheduler.remove_job(job_id)
                print(f"  - Removed job {job_id} (reminder likely sent or deleted).")

        # Wait before the next check
        await asyncio.sleep(30)


async def run_bot():
    signal_service = getenv("SIGNAL_SERVICE")
    phone_number = getenv("PHONE_NUMBER")

    config = {
        "signal_service": signal_service,
        "phone_number": phone_number,
        "storage": None,
    }
    bot = SignalBot(config)

    # enable a chat command for one specific group with the name "My Group"
    bot.register(ReminderCommand(), contacts=False, groups=["Reminders"])

    bot.start()


async def main():
    await asyncio.gather(run_bot(), run_scheduler())

if __name__ == "__main__":
    asyncio.run(main())
