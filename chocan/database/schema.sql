-- MANAGER
CREATE TABLE IF NOT EXISTS manager (
    manager_id  INTEGER PRIMARY KEY AUTOINCREMENT,
    name        TEXT NOT NULL
);

-- OPERATOR
CREATE TABLE IF NOT EXISTS operator (
    operator_id INTEGER PRIMARY KEY AUTOINCREMENT,
    name        TEXT NOT NULL,
    manager_id  INTEGER NOT NULL,
    FOREIGN KEY (manager_id) REFERENCES manager(manager_id)
);

-- MEMBER
CREATE TABLE IF NOT EXISTS member (
    member_no       INTEGER PRIMARY KEY,
    fname           TEXT NOT NULL,
    lname           TEXT NOT NULL,
    street_address  TEXT NOT NULL,
    city            TEXT NOT NULL,
    state           TEXT NOT NULL CHECK(length(state) = 2),
    zip             TEXT NOT NULL CHECK(length(zip) = 5),
    status          TEXT NOT NULL DEFAULT 'ACTIVE' CHECK(status IN ('ACTIVE', 'SUSPENDED'))
);

-- PROVIDER
CREATE TABLE IF NOT EXISTS provider (
    provider_no     INTEGER PRIMARY KEY,
    name            TEXT NOT NULL,
    street_address  TEXT NOT NULL,
    city            TEXT NOT NULL,
    state           TEXT NOT NULL CHECK(length(state) = 2),
    zip             TEXT NOT NULL CHECK(length(zip) = 5)
);

-- SERVICE
CREATE TABLE IF NOT EXISTS service (
    service_code    INTEGER PRIMARY KEY,
    service_name    TEXT NOT NULL,
    fee             REAL NOT NULL CHECK(fee > 0)
);

-- SERVICE_RECORD
CREATE TABLE IF NOT EXISTS service_record (
    record_id           INTEGER PRIMARY KEY AUTOINCREMENT,
    date_time_recorded  TEXT NOT NULL,
    date_service_provided TEXT NOT NULL,
    comments            TEXT,
    member_no           INTEGER NOT NULL,
    provider_no         INTEGER NOT NULL,
    service_code        INTEGER NOT NULL,
    FOREIGN KEY (member_no)     REFERENCES member(member_no),
    FOREIGN KEY (provider_no)   REFERENCES provider(provider_no),
    FOREIGN KEY (service_code)  REFERENCES service(service_code)
);

-- MEMBERSHIP_PAYMENT
CREATE TABLE IF NOT EXISTS membership_payment (
    payment_id      INTEGER PRIMARY KEY AUTOINCREMENT,
    amount          REAL NOT NULL CHECK(amount > 0),
    payment_date    TEXT NOT NULL,
    pay_status      TEXT NOT NULL CHECK(pay_status IN ('PAID', 'OVERDUE')),
    member_no       INTEGER NOT NULL,
    FOREIGN KEY (member_no) REFERENCES member(member_no)
);

-- BANK_ACCOUNT
CREATE TABLE IF NOT EXISTS bank_account (
    account_no      TEXT PRIMARY KEY,
    bank_name       TEXT NOT NULL,
    routing_no      TEXT NOT NULL CHECK(length(routing_no) = 9),
    provider_no     INTEGER NOT NULL UNIQUE,
    FOREIGN KEY (provider_no) REFERENCES provider(provider_no)
);

-- ACME_ACCOUNTING
CREATE TABLE IF NOT EXISTS acme_accounting (
    acme_id     INTEGER PRIMARY KEY AUTOINCREMENT,
    org_name    TEXT NOT NULL
);