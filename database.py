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
        
    def is_bssid_already_saved(self, bssid=None):
        if not bssid:
            print("[-] No BSSID provided to check.")
            return False
        
        result = self.execute_query("SELECT 1 FROM accesspoints WHERE bssid = ? UNION SELECT 1 FROM stations WHERE bssid = ? LIMIT 1", (bssid, bssid))

        if result:
            return True
        return False

    def close_connection(self):
        if self.db:
            self.db.close()
            print("[+] Database connection closed.")
        else:
            print("[-] No database connection to close.")


