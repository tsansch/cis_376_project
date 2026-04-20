# Program Name:   provider_directory.py
# Programmer Name: Tristan Elizalde
# Description:     Generates an alphabetically sorted directory of all available
#                  ChocAn services and writes it to a local file on provider request.
#                  Service data is read from the ChocAn SQLite database (service table).
# Date Created:    April 4th, 2026

import sqlite3
import datetime

from database.db_setup import get_connection


# Description:    Load all service records from the database.
# Pre-condition:  chocan.db exists and is initialized (see database/db_setup.py).
# Post-condition: Returns a list of service dicts with keys service_code,
#                 service_name, and fee; or an empty list if none exist or on error.
def load_services():
    try:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("SELECT service_code, service_name, fee FROM service")
        rows = cur.fetchall()
        conn.close()
        return [
            {"service_code": row[0], "service_name": row[1], "fee": row[2]}
            for row in rows
        ]
    except sqlite3.Error as e:
        print(f"Database error while loading services: {e}")
        return []


# Description:    Insert a single service into the database (for local testing).
# Pre-condition:  service_code is unique, fee > 0 per schema CHECK constraint.
# Post-condition: A new row exists in service, or an error message is shown.
def add_service(service_name, service_code, fee):
    try:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO service (service_code, service_name, fee) VALUES (?, ?, ?)",
            (int(service_code), service_name, float(fee)),
        )
        conn.commit()
        conn.close()
        return True
    except sqlite3.IntegrityError:
        print("Error: That service code already exists or violates database rules.")
        return False
    except sqlite3.Error as e:
        print(f"Database error while adding service: {e}")
        return False


# Description:    Generate an alphabetically sorted directory of all services
#                 and write it to a local file named after the provider and date.
# Pre-condition:  provider_name must be a valid non-empty string.
# Post-condition: A text file is created on the local disk and True is returned
#                 on success. If no services exist, or a file/unexpected error
#                 occurs, an error message is displayed and False is returned.
def generate_provider_directory(provider_name):
    try:
        services = load_services()

        if not services:
            print("No services available.")
            return False

        sorted_services = sorted(
            services, key=lambda x: x["service_name"].lower()
        )

        current_date = datetime.datetime.now().strftime("%m-%d-%Y")
        safe_provider_name = provider_name.replace(" ", "_")
        filename = f"{safe_provider_name}_{current_date}.txt"

        with open(filename, "w") as file:
            file.write(f"Provider Directory for {provider_name}\n")
            file.write(f"Generated on: {current_date}\n")
            file.write("-" * 50 + "\n")
            file.write(f"{'Service Name'.ljust(25)} | {'Code'.ljust(10)} | {'Fee'}\n")
            file.write("-" * 50 + "\n")
            for service in sorted_services:
                name = service["service_name"].ljust(25)
                code = str(service["service_code"]).zfill(6).ljust(10)
                fee = f"${float(service['fee']):.2f}"
                file.write(f"{name} | {code} | {fee}\n")

        print(f"Directory successfully generated and saved as: {filename}")
        return True

    except IOError:
        print("Error: Could not write directory file to disk.")
        return False

    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return False


# Description:    Interactive terminal menu for provider directory operations.
# Pre-condition:  None; all data comes from user input at runtime.
# Post-condition: Performs the chosen operation and loops until user exits.
def provider_directory_menu():
    while True:
        print("\n--- Provider Directory ---")
        print("1. Generate Provider Directory")
        print("2. View All Services")
        print("3. Add Service (for testing)")
        print("4. Exit")
        choice = input("Select an option: ").strip()

        if choice == "1":
            name = input("Enter provider name: ").strip()
            generate_provider_directory(name)

        elif choice == "2":
            services = load_services()
            if not services:
                print("No services found.")
            else:
                print(f"\n{'Service Name'.ljust(25)} | {'Code'.ljust(10)} | Fee")
                print("-" * 50)
                for s in sorted(
                    services, key=lambda x: x["service_name"].lower()
                ):
                    print(
                        f"{s['service_name'].ljust(25)} | "
                        f"{str(s['service_code']).zfill(6).ljust(10)} | "
                        f"${float(s['fee']):.2f}"
                    )

        elif choice == "3":
            name = input("Service name: ").strip()
            code = input("Service code (6 digits): ").strip()
            fee = input("Fee (e.g. 49.99): ").strip()
            if add_service(name, code, fee):
                print(f"Service '{name}' added.")

        elif choice == "4":
            break

        else:
            print("Invalid option. Please try again.")


if __name__ == "__main__":
    provider_directory_menu()
