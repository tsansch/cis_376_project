# Program Name:    member_manager.py
# Programmer Name: Era Shkembi
# Description:     Manages member validation and CRUD record management
#                  for the ChocAn system using the SQLite database (chocan.db).
# Date Created:    April 2026
 
from database import get_connection
 
 
# Description:   Validate a member number against the database.
# Pre-condition:  member_no is a string entered by the provider terminal.
# Post-condition: Returns "Validated", "Member suspended", or "Invalid number".
def validate_member(member_no):
    if not str(member_no).isdigit() or len(str(member_no)) != 9:
        return "Invalid number"
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT status FROM member WHERE member_no = ?", (int(member_no),))
    row = cur.fetchone()
    conn.close()
    if row is None:
        return "Invalid number"
    if row[0] == "SUSPENDED":
        return "Member suspended"
    return "Validated"
 
 
# Description:   Add a new member record to the database.
# Pre-condition:  member_no is a 9-digit integer not already in the database;
#                 fname, lname, street_address, city are non-empty strings;
#                 state is exactly 2 letters; zip is exactly 5 digits.
# Post-condition: New member row is inserted; returns True on success, False otherwise.
def add_member(member_no, fname, lname, street_address, city, state, zip_code, status="ACTIVE"):
    if not str(member_no).isdigit() or len(str(member_no)) != 9:
        print("Error: Member number must be exactly 9 digits.")
        return False
    if len(state) != 2:
        print("Error: State must be exactly 2 letters.")
        return False
    if len(zip_code) != 5 or not zip_code.isdigit():
        print("Error: ZIP code must be exactly 5 digits.")
        return False
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT member_no FROM member WHERE member_no = ?", (int(member_no),))
    if cur.fetchone():
        print("Error: Member number already exists.")
        conn.close()
        return False
    cur.execute(
        "INSERT INTO member (member_no, fname, lname, street_address, city, state, zip, status) "
        "VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
        (int(member_no), fname, lname, street_address, city, state.upper(), zip_code, status.upper())
    )
    conn.commit()
    conn.close()
    print(f"Member {member_no} added successfully.")
    return True
 
 
# Description:   Update a single field of an existing member record in the database.
# Pre-condition:  member_no exists in the member table; field is a valid column name;
#                 new_value satisfies the column CHECK constraint.
# Post-condition: The field is updated in the database; returns True on success.
def update_member(member_no, field, new_value):
    valid_fields = ["fname", "lname", "street_address", "city", "state", "zip", "status"]
    if field not in valid_fields:
        print(f"Error: Invalid field '{field}'.")
        return False
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT member_no FROM member WHERE member_no = ?", (int(member_no),))
    if not cur.fetchone():
        print("Error: Member not found.")
        conn.close()
        return False
    cur.execute(f"UPDATE member SET {field} = ? WHERE member_no = ?", (new_value, int(member_no)))
    conn.commit()
    conn.close()
    print(f"Member {member_no} updated: {field} = {new_value}")
    return True
 
 
# Description:   Delete a member record from the database.
# Pre-condition:  member_no must exist in the member table.
# Post-condition: Member row is removed; returns True on success, False if not found.
def delete_member(member_no):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT member_no FROM member WHERE member_no = ?", (int(member_no),))
    if not cur.fetchone():
        print("Error: Member not found.")
        conn.close()
        return False
    cur.execute("DELETE FROM member WHERE member_no = ?", (int(member_no),))
    conn.commit()
    conn.close()
    print(f"Member {member_no} deleted successfully.")
    return True
 
 
# Description:   Interactive terminal menu for all member management operations.
# Pre-condition:  Database must be initialized via database.init_db() before use.
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
            fname = input("First name: ").strip()
            lname = input("Last name: ").strip()
            addr  = input("Street address: ").strip()
            city  = input("City: ").strip()
            state = input("State (2 letters): ").strip()
            zipc  = input("ZIP code (5 digits): ").strip()
            add_member(num, fname, lname, addr, city, state, zipc)
        elif choice == "3":
            num   = input("Member number: ").strip()
            print("Valid fields: fname, lname, street_address, city, state, zip, status")
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
