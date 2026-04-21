# Program Name:    provider_manager.py
# Programmer Name: Era Shkembi
# Description:     Manages provider CRUD record management for the ChocAn
#                  system using the SQLite database (chocan.db).
# Date Created:    April 11 2026
 
from database.db_setup import get_connection
 
 
# Description:   Add a new provider record to the database.
# Pre-condition:  provider_no is a 9-digit integer not already in the database;
#                 name, street_address, city are non-empty strings;
#                 state is exactly 2 letters; zip is exactly 5 digits.
# Post-condition: New provider row is inserted; returns True on success, False otherwise.
def add_provider(provider_no, name, street_address, city, state, zip_code):
    if not str(provider_no).isdigit() or len(str(provider_no)) != 9:
        print("Error: Provider number must be exactly 9 digits.")
        return False
    if len(state) != 2:
        print("Error: State must be exactly 2 letters.")
        return False
    if len(zip_code) != 5 or not zip_code.isdigit():
        print("Error: ZIP code must be exactly 5 digits.")
        return False
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT provider_no FROM provider WHERE provider_no = ?", (int(provider_no),))
    if cur.fetchone():
        print("Error: Provider number already exists.")
        conn.close()
        return False
    cur.execute(
        "INSERT INTO provider (provider_no, name, street_address, city, state, zip) "
        "VALUES (?, ?, ?, ?, ?, ?)",
        (int(provider_no), name, street_address, city, state.upper(), zip_code)
    )
    conn.commit()
    conn.close()
    print(f"Provider {provider_no} added successfully.")
    return True
 
 
# Description:   Update a single field of an existing provider record in the database.
# Pre-condition:  provider_no exists in the provider table; field is a valid column name;
#                 new_value satisfies the column CHECK constraint.
# Post-condition: The field is updated in the database; returns True on success.
def update_provider(provider_no, field, new_value):
    valid_fields = ["name", "street_address", "city", "state", "zip"]
    if field not in valid_fields:
        print(f"Error: Invalid field '{field}'.")
        return False
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT provider_no FROM provider WHERE provider_no = ?", (int(provider_no),))
    if not cur.fetchone():
        print("Error: Provider not found.")
        conn.close()
        return False
    cur.execute(f"UPDATE provider SET {field} = ? WHERE provider_no = ?", (new_value, int(provider_no)))
    conn.commit()
    conn.close()
    print(f"Provider {provider_no} updated: {field} = {new_value}")
    return True
 
 
# Description:   Delete a provider record from the database.
# Pre-condition:  provider_no must exist in the provider table.
# Post-condition: Provider row is removed; returns True on success, False if not found.
def delete_provider(provider_no):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT provider_no FROM provider WHERE provider_no = ?", (int(provider_no),))
    if not cur.fetchone():
        print("Error: Provider not found.")
        conn.close()
        return False
    cur.execute("DELETE FROM provider WHERE provider_no = ?", (int(provider_no),))
    conn.commit()
    conn.close()
    print(f"Provider {provider_no} deleted successfully.")
    return True
 
 
# Description:   Interactive terminal menu for all provider management operations.
# Pre-condition:  Database must be initialized via database.init_db() before use.
# Post-condition: Performs the chosen operation and loops until user exits.
def provider_management_menu():
    while True:
        print("\n--- Provider Management ---")
        print("1. Add Provider")
        print("2. Update Provider")
        print("3. Delete Provider")
        print("4. Exit")
        choice = input("Select an option: ").strip()
        if choice == "1":
            num   = input("Provider number (9 digits): ").strip()
            name  = input("Name: ").strip()
            addr  = input("Street address: ").strip()
            city  = input("City: ").strip()
            state = input("State (2 letters): ").strip()
            zipc  = input("ZIP code (5 digits): ").strip()
            add_provider(num, name, addr, city, state, zipc)
        elif choice == "2":
            num   = input("Provider number: ").strip()
            print("Valid fields: name, street_address, city, state, zip")
            field = input("Field to update: ").strip()
            val   = input("New value: ").strip()
            update_provider(num, field, val)
        elif choice == "3":
            num = input("Provider number to delete: ").strip()
            delete_provider(num)
        elif choice == "4":
            break
        else:
            print("Invalid option. Please try again.")
 
 
if __name__ == "__main__":
    provider_management_menu()

