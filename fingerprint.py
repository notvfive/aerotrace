from database import DatabaseConnector
import hashlib, sys

db = DatabaseConnector("database.db").connect()
if not db:
    sys.exit(1)

class Fingerprint:
    @staticmethod
    async def Generate(data=None):
        if not data:
            print("[*] Failed to create a fingerprint. (Empty data given)")
            return ""

        _fingerprint = ""
        for key in data:
            _fingerprint += f"{key}_"

        hash = hashlib.md5()
        hash.update(_fingerprint.encode("UTF-8"))

        return hash.hexdigest()

    @staticmethod
    async def DoesFingerprintExist(fingerprint=None):
        if not fingerprint:
            print("[*] Failed to supply a fingerprint.")
            return None
        
        result = await db.execute_query(
            "SELECT fingerprint FROM accesspoints UNION SELECT fingerprint FROM stations;"
        )

        for fp in result:
            if fp[0].lower() == fingerprint.lower():
                return True

        return False
