# Program Name: main.py
# Programmer Name: ChocAn Development Team
# Description: Main entry point for the ChocAn data processing system.
#              Launches the interactive console loop and connects all modules.
# Date Created: 04/20/2026

from database.db_setup import init_db, seed_db
from validate_member import validate_member
from service_transaction import record_service
from member_manager import member_management_menu
from provider_manager import provider_management_menu
from provider_directory import provider_directory_menu
from report_generator import run_weekly_reports
from scheduler import start_scheduler


# Description: Displays the provider terminal menu and handles provider workflow
# Pre-condition: Database must be initialized
# Post-condition: Provider can validate a member and record a service
def provider_menu():
    print("\n=== Provider Terminal ===")
    provider_no = input("  Enter your 9-digit provider number: ").strip()
    if not provider_no.isdigit() or len(provider_no) != 9:
        print("  Invalid provider number.")
        return

    # validate member first (UC-1), then record service (UC-2)
    member_no = validate_member()
    if member_no:
        record_service(int(member_no), int(provider_no))


# Description: Displays the manager terminal menu
# Pre-condition: Database must be initialized
# Post-condition: Manager can run reports or view system status
def manager_menu():
    while True:
        print("\n=== Manager Terminal ===")
        print("1. Run Weekly Reports")
        print("2. Back")
        choice = input("Select option: ").strip()
        if choice == "1":
            run_weekly_reports()
        elif choice == "2":
            break
        else:
            print("  Invalid option.")


# Description: Displays the operator terminal menu
# Pre-condition: Database must be initialized
# Post-condition: Operator can manage member and provider records
def operator_menu():
    while True:
        print("\n=== Operator Terminal ===")
        print("1. Member Management")
        print("2. Provider Management")
        print("3. Provider Directory")
        print("4. Back")
        choice = input("Select option: ").strip()
        if choice == "1":
            member_management_menu()
        elif choice == "2":
            provider_management_menu()
        elif choice == "3":
            provider_directory_menu()
        elif choice == "4":
            break
        else:
            print("  Invalid option.")


# Description: Main system entry point. Initializes database, starts scheduler,
#              and launches the main menu loop.
# Pre-condition: Python 3 installed, all modules present in chocan/ directory
# Post-condition: System runs until user exits
def main():
    print("=== ChocAn Data Processing System ===")
    init_db()

    # start background scheduler for 9 PM Acme update and midnight Friday batch
    start_scheduler()

    while True:
        print("\n=== Main Menu ===")
        print("1. Provider Login")
        print("2. Manager Login")
        print("3. Operator Login")
        print("4. Exit")
        choice = input("Select option: ").strip()

        if choice == "1":
            provider_menu()
        elif choice == "2":
            manager_menu()
        elif choice == "3":
            operator_menu()
        elif choice == "4":
            print("Exiting ChocAn system.")
            break
        else:
            print("  Invalid option.")


if __name__ == "__main__":
    main()