DROP TABLE IF EXISTS accounts;
DROP TABLE IF EXISTS prevPasswords;
CREATE TABLE accounts (first_name TEXT, last_name TEXT, username TEXT UNIQUE NOT NULL, email_address TEXT UNIQUE NOT NULL, password TEXT, salt TEXT);
CREATE TABLE prevPasswords(username TEXT, prev_password TEXT, Primary KEY(prev_password, username));
