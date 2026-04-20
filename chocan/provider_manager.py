# Program Name:    provider_manager.py
# Programmer Name: Era Shkembi
# Description:     Manages provider records (add, update, delete) for the
#                  ChocAn data center system (UC-5).
# Date Created:    April 2026
 
import json
import os
 
PROVIDERS_FILE = "providers.json"
 
 
# Description:   Load all provider records from the JSON data file.
# Pre-condition:  providers.json should exist in the working directory.
# Post-condition: Returns a dict of provider records keyed by provider number,
#                 or an empty dict if the file does not exist.
def load_providers():
    if not os.path.exists(PROVIDERS_FILE):
        return {}
    with open(PROVIDERS_FILE, "r") as f:
        return json.load(f)
 
 
# Description:   Persist the provider records dict to the JSON data file.
# Pre-condition:  providers is a valid dict of provider record dicts.
# Post-condition: providers.json is overwritten with the current records.
def save_providers(providers):
    with open(PROVIDERS_FILE, "w") as f:
        json.dump(providers, f, indent=4)
 
 
# Description:   Add a new provider record to the data file.
# Pre-condition:  provider_number is a 9-digit string not already in the file;
#                 all other fields are non-empty strings.
# Post-condition: New provider is saved; returns True on success, False otherwise.
def add_provider(provider_number, name, address, city, state, zip_code):
    if not provider_number.isdigit() or len(provider_number) != 9:
        print("Error: Provider number must be exactly 9 digits.")
        return False
    providers = load_providers()
    if provider_number in providers:
        print("Error: Provider number already exists.")
        return False
    providers[provider_number] = {
        "name": name,
        "address": address,
        "city": city,
        "state": state,
        "zip_code": zip_code
    }
    save_providers(providers)
    print(f"Provider {provider_number} added successfully.")
    return True
 
 
# Description:   Update a single field of an existing provider record.
# Pre-condition:  provider_number exists in providers.json; field is one of the
#                 valid field names; new_value is a non-empty string.
# Post-condition: The field is updated and saved; returns True on success.
def update_provider(provider_number, field, new_value):
    providers = load_providers()
    if provider_number not in providers:
        print("Error: Provider not found.")
        return False
    valid_fields = ["name", "address", "city", "state", "zip_code"]
    if field not in valid_fields:
        print(f"Error: Invalid field '{field}'.")
        return False
    providers[provider_number][field] = new_value
    save_providers(providers)
    print(f"Provider {provider_number} updated: {field} = {new_value}")
    return True
 
 
# Description:   Delete a provider record from the data file.
# Pre-condition:  provider_number must exist in providers.json.
# Post-condition: Provider is removed and file is saved; returns True on success.
def delete_provider(provider_number):
    providers = load_providers()
    if provider_number not in providers:
        print("Error: Provider not found.")
        return False
    del providers[provider_number]
    save_providers(providers)
    print(f"Provider {provider_number} deleted successfully.")
    return True
 
 
# Description:   Interactive terminal menu for all provider management operations.
# Pre-condition:  None; all data comes from user input at runtime.
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
            addr  = input("Address: ").strip()
            city  = input("City: ").strip()
            state = input("State (2 letters): ").strip()
            zipc  = input("ZIP code: ").strip()
            add_provider(num, name, addr, city, state, zipc)
        elif choice == "2":
            num   = input("Provider number: ").strip()
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
