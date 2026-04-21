# Program Name: acme_processor.py
# Programmer Name: Era Shkembi
# Description: Processes the nightly membership status update file received
#              from Acme Accounting Services at 9 PM. Reads the update file
#              and applies member status changes to the database.
# Date Created: 04/20/2026

import os
from database.db_setup import get_connection

ACME_UPDATE_FILE = "acme_update.txt"


# Description: Reads the Acme update file and returns a list of update records
# Pre-condition: acme_update.txt must exist in the working directory.
#                Each line must follow the format: member_no,status
# Post-condition: Returns a list of tuples (member_no, status), or empty list if file not found
def read_acme_file():
    if not os.path.exists(ACME_UPDATE_FILE):
        print(f"  Acme update file not found: {ACME_UPDATE_FILE}")
        return []
    records = []
    with open(ACME_UPDATE_FILE, "r") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            parts = line.split(",")
            if len(parts) == 2:
                member_no = parts[0].strip()
                status = parts[1].strip().upper()
                if status in ("ACTIVE", "SUSPENDED"):
                    records.append((member_no, status))
                else:
                    print(f"  Skipping invalid status for member {member_no}: {status}")
            else:
                print(f"  Skipping malformed line: {line}")
    return records


# Description: Updates a single member's status in the database
# Pre-condition: member_no must exist in the member table, status must be ACTIVE or SUSPENDED
# Post-condition: Member status is updated in the database. Returns True if successful, False otherwise
def update_member_status(member_no, status):
    try:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("UPDATE member SET status = ? WHERE member_no = ?", (status, int(member_no)))
        if cur.rowcount == 0:
            print(f"  Member {member_no} not found in database, skipping.")
            conn.close()
            return False
        conn.commit()
        conn.close()
        return True
    except Exception as e:
        print(f"  Error updating member {member_no}: {e}")
        return False


# Description: Main entry point for Acme nightly update. Reads the update file
#              and applies all status changes to the member table.
# Pre-condition: acme_update.txt must exist with valid format. Database must be accessible.
# Post-condition: All valid member statuses are updated. Logs completion or errors.
def process_acme_update():
    print("\n  Processing Acme nightly membership update...")
    records = read_acme_file()

    if not records:
        print("  No records to process.")
        return

    success = 0
    failed = 0
    for member_no, status in records:
        if update_member_status(member_no, status):
            success += 1
        else:
            failed += 1

    print(f"  Acme update complete. Updated: {success}, Failed/Skipped: {failed}")