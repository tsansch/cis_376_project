# Program Name: validate_member.py
# Programmer Name: Karim Joumaa
# Description: Handles member validation for the ChocAn data processing system.
#              Accepts a 9-digit member number from the provider, validates the
#              format, queries the member database, and displays Validated or an
#              appropriate rejection message.
# Date Created: 04/17/2026

from database.db_setup import get_connection


# Description: Validates that the member number string is exactly 9 digits

def validate_format(member_num):
    return member_num.isdigit() and len(member_num) == 9


# Description: Looks up a member in the database and returns their membership status
# Post-condition: Returns 'ACTIVE', 'SUSPENDED', None if the number is not found,
#                 or 'UNREACHABLE' if the database cannot be contacted

def lookup_member(member_num):
    try:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute(
            "SELECT status FROM member WHERE member_no = ?",
            (int(member_num),)
        )
        row = cur.fetchone()
        conn.close()
        if row:
            return row[0]
        return None
    except Exception:
        return "UNREACHABLE"


# Description: Main entry point for UC-1. Prompts the provider for a 9-digit member
#              number, validates the format, queries the database for status, and
#              displays the result. Loops until a definitive result is reached.


def validate_member():
    print("\nMember Validation")
    while True:
        member_input = input("  Enter member number: ").strip()

        if not validate_format(member_input):
            print("  Invalid format. Member number must be exactly 9 digits.")
            continue

        status = lookup_member(member_input)

        if status == "UNREACHABLE":
            print("  Data center unreachable. Please retry.")
            continue
        elif status is None:
            print("  Invalid number.")
            continue
        elif status == "SUSPENDED":
            print("  Member suspended.")
            return None
        elif status == "ACTIVE":
            print("  Validated.")
            return member_input
