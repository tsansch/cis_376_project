import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), "chocan.db")
SCHEMA_PATH = os.path.join(os.path.dirname(__file__), "schema.sql")


def get_connection(): 
    """Return a connection to the ChocAn database."""
    conn = sqlite3.connect(DB_PATH)
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def init_db():
    """Create all tables from schema.sql if they don't exist."""
    with open(SCHEMA_PATH, "r") as f:
        schema = f.read()
    conn = get_connection()
    conn.executescript(schema)
    conn.commit()
    conn.close()
    print("Database initialized.")


def seed_db():
    """
    DEV/TESTING ONLY - Insert sample data for local development and testing.
    Do not call this during the demo or final submission unless resetting test data.
    """
    conn = get_connection()
    cur = conn.cursor()

    # manager
    cur.execute("INSERT OR IGNORE INTO manager (manager_id, name) VALUES (1, 'Ali Manager')")

    # operator
    cur.execute("INSERT OR IGNORE INTO operator (operator_id, name, manager_id) VALUES (1, 'Aline Operator', 1)")

    # members
    cur.executemany("INSERT OR IGNORE INTO member VALUES (?,?,?,?,?,?,?,?)", [
        (123456789, 'Era',   'Shkembi', '123 Main St',    'Detroit',   'MI', '48201', 'ACTIVE'),
        (987654321, 'Karim', 'Joumaa',  '456 Oak Ave',    'Ann Arbor', 'MI', '48103', 'SUSPENDED'),
        (111222333, 'Tristan', 'Elizalde', '789 Pine Rd', 'Dearborn',  'MI', '48120', 'ACTIVE'),
    ])

    # providers
    cur.executemany("INSERT OR IGNORE INTO provider VALUES (?,?,?,?,?,?)", [
        (111111111, 'Dr. Ali Lee',   '100 Health Blvd', 'Detroit',   'MI', '48201'),
        (222222222, 'Dr. Aline Brown', '200 Care Lane', 'Ann Arbor', 'MI', '48103'),
    ])

    # services
    cur.executemany("INSERT OR IGNORE INTO service VALUES (?,?,?)", [
        (100001, 'Dietary Consultation', 75.00),
        (100002, 'Exercise Session',     50.00),
        (100003, 'Stress Management',    90.00),
        (100004, 'Nutrition Counseling', 65.00),
        (100005, 'Group Therapy',        45.00),
    ])

    # bank accounts
    cur.executemany("INSERT OR IGNORE INTO bank_account VALUES (?,?,?,?)", [
        ('ACC001', 'Chase Bank',  '021000021', 111111111),
        ('ACC002', 'Wells Fargo', '121042882', 222222222),
    ])

    # acme accounting
    cur.execute("INSERT OR IGNORE INTO acme_accounting (acme_id, org_name) VALUES (1, 'Acme Accounting Services')")

    conn.commit()
    conn.close()
    print("Seed data inserted.")


if __name__ == "__main__":
    init_db()
    seed_db()