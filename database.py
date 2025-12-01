import sqlite3
import os
import sys

class DatabaseConnector:
    def __init__(self, db_path):
        self.db_path = db_path
        self.db = None
        self.cur = None

    def connect(self):
        print("[*] Attempting to connect to the database...")

        if not os.path.exists(self.db_path):
            print("[-] Database file does not exist. Exiting.")
            sys.exit(1)

        try:
            self.db = sqlite3.connect(self.db_path)
            self.cur = self.db.cursor()
            print("[+] Database connection successful!")
            return self
        except sqlite3.Error as e:
            print(f"[-] Failed to connect to database: {e}")
            return sys.exit(1) or False

    def execute_query(self, query, params=None):
        if self.cur:
            try:
                if params:
                    self.cur.execute(query, params)
                else:
                    self.cur.execute(query)
                self.db.commit()
                return self.cur.fetchall()
            except sqlite3.Error as e:
                print(f"[-] Error executing query: {e}")
                return None
        else:
            print("[-] No database connection.")
            return None

    def close_connection(self):
        if self.db:
            self.db.close()
            print("[+] Database connection closed.")
        else:
            print("[-] No database connection to close.")

