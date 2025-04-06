from apscheduler.schedulers.blocking import BlockingScheduler
from datetime import datetime


def send_reminder_job(message, recipient):
    print(f"Sende '{message}' an {recipient} um {datetime.now()}")
    # Hier deine Sende-Logik einfügen
    # Optional: Markiere den Job in deiner primären DB/Datei als erledigt

    scheduler = BlockingScheduler(timezone="Europe/Berlin") # Wichtig: Zeitzone setzen!

    # Beispiel: Laden von Remindern beim Start und Planen
    reminders_from_storage = load_reminders()  # Deine Lade-Funktion
    for reminder in reminders_from_storage:
        if reminder_is_still_pending(reminder):  # Prüfen ob noch nicht gesendet
            run_time = datetime.fromisoformat(reminder['zeit'])
            # Füge Job hinzu, wenn er in der Zukunft liegt
            if run_time > datetime.now(run_time.tzinfo):
                 scheduler.add_job(send_reminder_job, 'date', run_date=run_time,
                                 args=[reminder['nachricht'], reminder['empfaenger']],
                                 id=f"reminder_{reminder['id']}") # Eindeutige ID ist gut

# Hier könntest du auch eine Funktion hinzufügen, um neue Reminder dynamisch zu planen

print("Scheduler gestartet... Drücke Ctrl+C zum Beenden.")
try:
    scheduler.start()
except (KeyboardInterrupt, SystemExit):
    pass