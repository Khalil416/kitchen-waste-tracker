"""One-off migration: hash any plaintext passwords in reg.db's users table.

Idempotent — rows already in 'iterations$salt$hash' form are left untouched,
so this is safe to re-run.

Usage:
    python tools/migrate_passwords.py
"""
import os
import sqlite3
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from backend.common.security import hash_password, is_hashed

REG_DB = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "reg.db")


def migrate(db_path: str = REG_DB) -> int:
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()
    cur.execute("SELECT id, username, password FROM users")
    rows = cur.fetchall()

    migrated = 0
    for user_id, username, password in rows:
        if is_hashed(password or ""):
            continue
        new_value = hash_password(password or "")
        cur.execute("UPDATE users SET password = ? WHERE id = ?", (new_value, user_id))
        migrated += 1
        print(f"  migrated user_id={user_id} username={username!r}")

    conn.commit()
    conn.close()
    return migrated


if __name__ == "__main__":
    count = migrate()
    print(f"Done. {count} row(s) migrated to hashed passwords.")
