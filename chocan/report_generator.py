# Program Name: report_generator.py
# Programmer Name: Karim Joumaa
# Description: Handles the weekly accounting batch procedure for the ChocAn system.
#              Reads all weekly service transaction records from the database,
#              generates member reports, provider reports, manager summary, and EFT file.
# Date Created: 04/17/2026

from datetime import datetime
from database.db_setup import get_connection


# Description: Queries all service transaction records written during the current week.
#              The week is defined as the 7 days leading up to the current run.
# Pre-condition: Database is accessible with service_record, member, provider, service tables
# Post-condition: Returns a list of row tuples for this week, or an empty list if none found

def read_weekly_transactions():
    try:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("""
            SELECT sr.date_service_provided,
                   sr.date_time_recorded,
                   sr.member_no,
                   sr.provider_no,
                   sr.service_code,
                   sr.comments,
                   m.fname || ' ' || m.lname,
                   m.street_address,
                   m.city,
                   m.state,
                   m.zip,
                   p.name,
                   p.street_address,
                   p.city,
                   p.state,
                   p.zip,
                   s.service_name,
                   s.fee
            FROM service_record sr
            JOIN member   m ON sr.member_no   = m.member_no
            JOIN provider p ON sr.provider_no = p.provider_no
            JOIN service  s ON sr.service_code = s.service_code
            WHERE sr.date_time_recorded >= date('now', 'weekday 5', '-7 days')
        """)
        rows = cur.fetchall()
        conn.close()
        return rows
    except Exception as e:
        print(f"  Database error: {e}")
        return []


# Description: Writes a member report file to disk for one member.
#              File name format is MemberName_MM-DD-YYYY.txt.
#              Services are listed in ascending order by date of service.
# Post-condition: Creates the report file on disk. Returns True if successful, False otherwise.

def write_member_report(member_data, report_date):
    name = member_data["name"][:25]
    filename = f"{name.replace(' ', '_')}_{report_date}.txt"
    try:
        sorted_services = sorted(member_data["services"], key=lambda x: x["date"])
        with open(filename, "w") as f:
            f.write(f"Member Name:      {name}\n")
            f.write(f"Member Number:    {member_data['number']}\n")
            f.write(f"Street Address:   {member_data['address'][:25]}\n")
            f.write(f"City:             {member_data['city'][:14]}\n")
            f.write(f"State:            {member_data['state'][:2]}\n")
            f.write(f"ZIP Code:         {member_data['zip'][:5]}\n\n")
            f.write("Services Received This Week:\n")
            for svc in sorted_services:
                f.write(f"  Date of Service:  {svc['date']}\n")
                f.write(f"  Provider Name:    {svc['provider_name'][:25]}\n")
                f.write(f"  Service Name:     {svc['service_name'][:20]}\n\n")
        return True
    except Exception as e:
        print(f"  Error writing member report for {name}: {e}")
        return False


# Description: Writes a provider report file to disk for one provider.
#              File name format is ProviderName_MM-DD-YYYY.txt.
#              Includes a summary of total consultations and total fee for the week.
# Post-condition: Creates the report file on disk. Returns True if successful, False otherwise.

def write_provider_report(provider_data, report_date):
    name = provider_data["name"][:25]
    filename = f"{name.replace(' ', '_')}_{report_date}.txt"
    try:
        total_fee = 0.0
        total_consults = 0
        with open(filename, "w") as f:
            f.write(f"Provider Name:    {name}\n")
            f.write(f"Provider Number:  {provider_data['number']}\n")
            f.write(f"Street Address:   {provider_data['address'][:25]}\n")
            f.write(f"City:             {provider_data['city'][:14]}\n")
            f.write(f"State:            {provider_data['state'][:2]}\n")
            f.write(f"ZIP Code:         {provider_data['zip'][:5]}\n\n")
            f.write("Services Billed This Week:\n")
            for svc in provider_data["services"]:
                f.write(f"  Date of Service:       {svc['date']}\n")
                f.write(f"  Date/Time Received:    {svc['recorded']}\n")
                f.write(f"  Member Name:           {svc['member_name'][:25]}\n")
                f.write(f"  Member Number:         {svc['member_no']}\n")
                f.write(f"  Service Code:          {svc['service_code']}\n")
                f.write(f"  Fee:                   ${svc['fee']:.2f}\n\n")
                total_fee += svc["fee"]
                total_consults += 1
            f.write(f"Total Consultations: {total_consults:>3}\n")
            f.write(f"Total Fee:           ${total_fee:.2f}\n")
        return True
    except Exception as e:
        print(f"  Error writing provider report for {name}: {e}")
        return False


# Description: Writes the manager summary report to disk.
#              Lists every provider paid that week with their consultation count and total fee,
#              followed by grand totals across all providers.
# Pre-condition: provider_summaries is a list of dicts with name, number, consultations, total_fee.
#                report_date is a string in MM-DD-YYYY format.

def write_manager_summary(provider_summaries, report_date):
    filename = f"Manager_Summary_{report_date}.txt"
    try:
        grand_consults = 0
        grand_fees = 0.0
        with open(filename, "w") as f:
            f.write("ChocAn Manager Summary Report\n")
            f.write(f"Report Date: {report_date}\n\n")
            for p in provider_summaries:
                f.write(f"Provider:        {p['name']}\n")
                f.write(f"  Consultations: {p['consultations']}\n")
                f.write(f"  Total Fee:     ${p['total_fee']:.2f}\n\n")
                grand_consults += p["consultations"]
                grand_fees += p["total_fee"]
            f.write(f"Total Providers:      {len(provider_summaries)}\n")
            f.write(f"Total Consultations:  {grand_consults}\n")
            f.write(f"Total Fees:           ${grand_fees:.2f}\n")
        return True
    except Exception as e:
        print(f"  Error writing manager summary: {e}")
        return False


# Description: Writes the EFT data file to disk.
#              Contains one record per provider: name, number, and amount to transfer.


def write_eft_file(provider_summaries, report_date):
    filename = f"EFT_Data_{report_date}.txt"
    try:
        with open(filename, "w") as f:
            f.write("ChocAn EFT Data\n")
            f.write(f"Report Date: {report_date}\n\n")
            for p in provider_summaries:
                f.write(f"Provider Name:      {p['name']}\n")
                f.write(f"Provider Number:    {p['number']}\n")
                f.write(f"Amount to Transfer: ${p['total_fee']:.2f}\n\n")
        return True
    except Exception as e:
        print(f"  Error writing EFT file: {e}")
        return False


# Description: Main entry point for UC-3. Locks interactive mode, reads all weekly
#              transaction records, and generates all required output files.
#              Halts immediately and logs the error if any file write fails.


def run_weekly_reports(lock_callback=None, unlock_callback=None):
    print("\nRunning Weekly Accounting Procedure")

    if lock_callback:
        lock_callback()

    report_date = datetime.now().strftime("%m-%d-%Y")
    transactions = read_weekly_transactions()

    if not transactions:
        print("  No transactions found this week. Generating zero-activity reports.")

    members = {}
    providers = {}

    for row in transactions:
        (date_svc, date_rec, mem_no, prov_no, svc_code, comments,
         mem_name, mem_addr, mem_city, mem_state, mem_zip,
         prov_name, prov_addr, prov_city, prov_state, prov_zip,
         svc_name, fee) = row

        if mem_no not in members:
            members[mem_no] = {
                "name": mem_name,
                "number": mem_no,
                "address": mem_addr,
                "city": mem_city,
                "state": mem_state,
                "zip": mem_zip,
                "services": []
            }
        members[mem_no]["services"].append({
            "date": date_svc,
            "provider_name": prov_name,
            "service_name": svc_name
        })

        if prov_no not in providers:
            providers[prov_no] = {
                "name": prov_name,
                "number": prov_no,
                "address": prov_addr,
                "city": prov_city,
                "state": prov_state,
                "zip": prov_zip,
                "services": []
            }
        providers[prov_no]["services"].append({
            "date": date_svc,
            "recorded": date_rec,
            "member_name": mem_name,
            "member_no": mem_no,
            "service_code": svc_code,
            "fee": fee
        })

    for mem_data in members.values():
        if not write_member_report(mem_data, report_date):
            print("  Batch halted due to file write error.")
            if unlock_callback:
                unlock_callback()
            return False

    provider_summaries = []
    for prov_data in providers.values():
        if not write_provider_report(prov_data, report_date):
            print("  Batch halted due to file write error.")
            if unlock_callback:
                unlock_callback()
            return False
        total_fee = sum(s["fee"] for s in prov_data["services"])
        provider_summaries.append({
            "name": prov_data["name"],
            "number": prov_data["number"],
            "consultations": len(prov_data["services"]),
            "total_fee": total_fee
        })

    if not write_manager_summary(provider_summaries, report_date):
        print("  Batch halted due to file write error.")
        if unlock_callback:
            unlock_callback()
        return False

    if not write_eft_file(provider_summaries, report_date):
        print("  Batch halted due to file write error.")
        if unlock_callback:
            unlock_callback()
        return False

    print("  Weekly accounting procedure completed successfully.")
    print(f"  Reports saved with date: {report_date}")
    if unlock_callback:
        unlock_callback()
    return True
