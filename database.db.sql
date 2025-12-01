BEGIN TRANSACTION;
CREATE TABLE IF NOT EXISTS "accesspoints" (
	"id"	INTEGER,
	"bssid"	TEXT,
	"ssid"	TEXT,
	"encryption"	TEXT,
	"vendor"	TEXT,
	"avg_strength"	INTEGER,
	"fingerprint"	TEXT,
	PRIMARY KEY("id" AUTOINCREMENT)
);
CREATE TABLE IF NOT EXISTS "stations" (
	"id"	INTEGER,
	"bssid"	TEXT,
	"vendor"	TEXT,
	"fingerprint"	TEXT,
	PRIMARY KEY("id" AUTOINCREMENT)
);
COMMIT;
