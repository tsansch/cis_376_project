# Program Name: scheduler.py
# Programmer Name: Tristan Elizalde
# Description: Background scheduler for the ChocAn system. Triggers the Acme
#              membership update at 9:00 PM daily and the weekly accounting
#              batch procedure at midnight every Friday automatically.
# Date Created: 04/20/2026

import threading
import time
from datetime import datetime


# Description: Checks the current time and triggers scheduled tasks if their
#              run conditions are met. Runs in a background thread every 60 seconds.
# Pre-condition: report_generator and acme_processor modules must be importable
# Post-condition: Scheduled tasks fire at their defined times without manual intervention
def scheduler_loop():
    acme_ran_today = None
    batch_ran_this_week = None

    while True:
        now = datetime.now()
        today = now.date()
        current_hour = now.hour
        current_minute = now.minute
        current_weekday = now.weekday()  # 4 = Friday

        # run Acme update at 9:00 PM daily
        if current_hour == 21 and current_minute == 0:
            if acme_ran_today != today:
                print("\n  [Scheduler] Triggering Acme nightly update (9:00 PM)")
                try:
                    from acme_processor import process_acme_update
                    process_acme_update()
                    acme_ran_today = today
                except Exception as e:
                    print(f"  [Scheduler] Acme update error: {e}")

        # run weekly batch at midnight Friday (weekday 4, hour 0, minute 0)
        if current_weekday == 4 and current_hour == 0 and current_minute == 0:
            week_key = now.isocalendar()[1]  # ISO week number
            if batch_ran_this_week != week_key:
                print("\n  [Scheduler] Triggering weekly accounting batch (midnight Friday)")
                try:
                    from report_generator import run_weekly_reports
                    run_weekly_reports()
                    batch_ran_this_week = week_key
                except Exception as e:
                    print(f"  [Scheduler] Batch error: {e}")

        # check every 60 seconds
        time.sleep(60)


# Description: Starts the scheduler in a background daemon thread so it runs
#              alongside the interactive console without blocking it.
# Pre-condition: Called once at system startup from main.py
# Post-condition: Scheduler thread is running in the background. Returns immediately.
def start_scheduler():
    scheduler_thread = threading.Thread(target=scheduler_loop, daemon=True)
    scheduler_thread.start()
    print("  [Scheduler] Background scheduler started.")