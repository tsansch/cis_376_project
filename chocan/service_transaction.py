# Program Name: service_transaction.py
# Programmer Name: Adam Hammoud
# Description: Handles service logging and fee lookup for the ChocAn system.
#              Accepts provider input, validates service codes, writes transaction
#              records to the database, and displays the service fee.
# Date Created: 04/19/2026

import sqlite3
import re
from datetime import datetime
from database.db_setup import get_connection


# Description: Validates that the date string is in MM-DD-YYYY format
# Pre-condition: date_str is a string entered by the provider
# Post-condition: Returns True if format is valid, False otherwise

def validate_date(date_str):
    pattern = r'^\d{2}-\d{2}-\d{4}$'
    if not re.match(pattern, date_str):
        return False
    try:
        datetime.strptime(date_str, "%m-%d-%Y")
        return True
    except ValueError:
        return False


# Description: Validates that the service code is exactly 6 digits
# Pre-condition: code is a string entered by the provider
# Post-condition: Returns True if code is 6 digits, False otherwise

def validate_service_code(code):
    return code.isdigit() and len(code) == 6


# Description: Looks up a service code in the database and returns the service record
# Pre-condition: service_code is a valid 6-digit string
# Post-condition: Returns a dict with service_name and fee if found, None otherwise

def lookup_service(service_code):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT service_name, fee FROM service WHERE service_code = ?", (int(service_code),))
    row = cur.fetchone()
    conn.close()
    if row:
        return {"service_name": row[0], "fee": row[1]}
    return None


# Description: Writes a complete transaction record to the database
# Pre-condition: All fields must be provided. member_no and provider_no must exist in DB.
#               service_code must exist in the service table. comments can be empty string.
# Post-condition: A new row is inserted into service_record table. Returns True if successful, False otherwise.

def write_transaction(date_service_provided, provider_no, member_no, service_code, comments):
    date_time_recorded = datetime.now().strftime("%m-%d-%Y %H:%M:%S")
    conn = get_connection()
    cur = conn.cursor()
    try:
        cur.execute("""
            INSERT INTO service_record 
            (date_time_recorded, date_service_provided, comments, member_no, provider_no, service_code)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (date_time_recorded, date_service_provided, comments, member_no, provider_no, int(service_code)))
        conn.commit()
        return True
    except Exception as e:
        print(f"  Error writing transaction: {e}")
        return False
    finally:
        conn.close()


# Description: Displays the fee for a given service code
# Pre-condition: service_code must exist in the database
# Post-condition: Prints the fee to the screen

def display_fee(service_code):
    service = lookup_service(service_code)
    if service:
        print(f"\n  Fee billed to ChocAn: ${service['fee']:.2f}")


# Description: Main flow for recording a service transaction.
#              Runs after UC-1 (member validation) has completed successfully.
# Pre-condition: member_no and provider_no are valid and already in session
# Post-condition: A transaction record is written to the database and fee is displayed

def record_service(member_no, provider_no):
    print("\n--- Record Service ---")

    # get date of service from provider and validate format
    while True:
        date_input = input("  Enter date of service (MM-DD-YYYY): ").strip()
        if validate_date(date_input):
            break
        print("  Invalid date format. Please use MM-DD-YYYY.")

    # get service code, validate format, and look up service name
    while True:
        code_input = input("  Enter 6-digit service code: ").strip()
        if not validate_service_code(code_input):
            print("  Invalid code format. Must be exactly 6 digits.")
            continue
        service = lookup_service(code_input)
        if not service:
            print("  Service code not found. Please try again.")
            continue

        # confirm service name with provider before proceeding
        print(f"  Service name: {service['service_name']}")
        confirm = input("  Is this correct? (y/n): ").strip().lower()
        if confirm == 'y':
            break
        print("  Please re-enter the service code.")

    # get optional comments from provider, limit to 100 characters
    comments = input("  Enter comments (optional, press Enter to skip): ").strip()
    if len(comments) > 100:
        comments = comments[:100]
        print("  Comments truncated to 100 characters.")

    # write transaction to database
    success = write_transaction(date_input, provider_no, member_no, code_input, comments)
    if not success:
        print("  Failed to save transaction. Please try again.")
        return

    print("  Transaction recorded successfully.")

    # display the fee for the recorded service
    display_fee(code_input)