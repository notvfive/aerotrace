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

    async def execute_query(self, query, params=None):
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
        
    async def is_bssid_already_saved(self, bssid=None):
        if not bssid:
            print("[-] No BSSID provided to check.")
            return False
        
        result = await self.execute_query("SELECT 1 FROM accesspoints WHERE bssid = ? UNION SELECT 1 FROM stations WHERE bssid = ? LIMIT 1", (bssid, bssid))

        if result:
            return True
        return False
    
    async def is_ssid_already_saved(self, ssid=None):
        if not ssid:
            print("[-] No SSID provided to check.")
            return False
        
        result = await self.execute_query("SELECT 1 FROM accesspoints WHERE ssid = ? UNION SELECT 1 FROM stations WHERE ssid = ? LIMIT 1", (ssid, ssid))

        if result:
            return True
        return False
    
    async def get_bssid_from_ssid(self, ssid=None):
        if not ssid:
            print("[-] No SSID provided to check.")
            return []

        result = await self.execute_query("SELECT bssid FROM accesspoints WHERE ssid = ? UNION SELECT bssid FROM stations WHERE ssid = ?", (ssid, ssid))

        if result:
            return [row[0] for row in result]
        
        return []
    
    async def get_ssid_from_bssid(self, bssid=None):
        if not bssid:
            print("[-] No BSSID provided to check.")
            return []

        result = await self.execute_query("SELECT ssid FROM accesspoints WHERE bssid = ? UNION SELECT ssid FROM stations WHERE bssid = ?", (bssid, bssid))

        if result:
            return [row[0] for row in result]
        
        return []

    async def close_connection(self):
        if self.db:
            self.db.close()
            print("[+] Database connection closed.")
        else:
            print("[-] No database connection to close.")
    
    def check_column_existence(self, table_name, column_name):
        if not self.cur:
            print("[-] No database connection.")
            return False
        try:
            self.cur.execute(f"PRAGMA table_info({table_name})")
            columns = self.cur.fetchall()
            for col in columns:
                if col[1] == column_name:
                    return True
            return False
        except sqlite3.Error as e:
            print(f"[-] Error checking table schema: {e}")
            return False