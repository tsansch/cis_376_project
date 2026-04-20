# Program Name:    member_manager.py
# Programmer Name: Era Shkembi
# Description:     Handles member validation and CRUD record management
#                  for the ChocAn data center system.
# Date Created:    April 2026
 
import json
import os
 
MEMBERS_FILE = "members.json"
 
 
# Description:   Load all member records from the JSON data file.
# Pre-condition:  members.json should exist in the working directory.
# Post-condition: Returns a dict of member records keyed by member number,
#                 or an empty dict if the file does not exist.
def load_members():
    if not os.path.exists(MEMBERS_FILE):
        return {}
    with open(MEMBERS_FILE, "r") as f:
        return json.load(f)
 
 
# Description:   Persist the member records dict to the JSON data file.
# Pre-condition:  members is a valid dict of member record dicts.
# Post-condition: members.json is overwritten with the current records.
def save_members(members):
    with open(MEMBERS_FILE, "w") as f:
        json.dump(members, f, indent=4)
 
 
# Description:   Validate a member number against stored records and status.
# Pre-condition:  member_number is a string provided by the caller.
# Post-condition: Returns "Validated", "Member suspended", or "Invalid number".
def validate_member(member_number):
    if not member_number.isdigit() or len(member_number) != 9:
        return "Invalid number"
    members = load_members()
    if member_number not in members:
        return "Invalid number"
    if members[member_number].get("status") == "suspended":
        return "Member suspended"
    return "Validated"
 
 
# Description:   Add a new member record to the data file.
# Pre-condition:  member_number is a 9-digit string not already in the file;
#                 all other fields are non-empty strings.
# Post-condition: New member is saved; returns True on success, False otherwise.
def add_member(member_number, name, address, city, state, zip_code, status="active"):
    if not member_number.isdigit() or len(member_number) != 9:
        print("Error: Member number must be exactly 9 digits.")
        return False
    members = load_members()
    if member_number in members:
        print("Error: Member number already exists.")
        return False
    members[member_number] = {
        "name": name, "address": address, "city": city,
        "state": state, "zip_code": zip_code, "status": status
    }
    save_members(members)
    print(f"Member {member_number} added successfully.")
    return True
 
 
# Description:   Update a single field of an existing member record.
# Pre-condition:  member_number exists in members.json; field is one of the
#                 valid field names; new_value is a non-empty string.
# Post-condition: The field is updated and saved; returns True on success.
def update_member(member_number, field, new_value):
    members = load_members()
    if member_number not in members:
        print("Error: Member not found.")
        return False
    valid_fields = ["name", "address", "city", "state", "zip_code", "status"]
    if field not in valid_fields:
        print(f"Error: Invalid field '{field}'.")
        return False
    members[member_number][field] = new_value
    save_members(members)
    print(f"Member {member_number} updated: {field} = {new_value}")
    return True
 
 
# Description:   Delete a member record from the data file.
# Pre-condition:  member_number must exist in members.json.
# Post-condition: Member is removed and file is saved; returns True on success.
def delete_member(member_number):
    members = load_members()
    if member_number not in members:
        print("Error: Member not found.")
        return False
    del members[member_number]
    save_members(members)
    print(f"Member {member_number} deleted successfully.")
    return True
 
 
# Description:   Interactive terminal menu for all member management operations.
# Pre-condition:  None; all data comes from user input at runtime.
# Post-condition: Performs the chosen operation and loops until user exits.
def member_management_menu():
    while True:
        print("\n--- Member Management ---")
        print("1. Validate Member")
        print("2. Add Member")
        print("3. Update Member")
        print("4. Delete Member")
        print("5. Exit")
        choice = input("Select an option: ").strip()
        if choice == "1":
            num = input("Enter member number: ").strip()
            print(validate_member(num))
        elif choice == "2":
            num   = input("Member number (9 digits): ").strip()
            name  = input("Name: ").strip()
            addr  = input("Address: ").strip()
            city  = input("City: ").strip()
            state = input("State (2 letters): ").strip()
            zipc  = input("ZIP code: ").strip()
            add_member(num, name, addr, city, state, zipc)
        elif choice == "3":
            num   = input("Member number: ").strip()
            field = input("Field to update: ").strip()
            val   = input("New value: ").strip()
            update_member(num, field, val)
        elif choice == "4":
            num = input("Member number to delete: ").strip()
            delete_member(num)
        elif choice == "5":
            break
        else:
            print("Invalid option. Please try again.")
 
 
if __name__ == "__main__":
    member_management_menu()
