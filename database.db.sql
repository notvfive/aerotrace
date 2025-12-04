BEGIN TRANSACTION;
CREATE TABLE IF NOT EXISTS "accesspoints" (
	"id"	INTEGER,
	"bssid"	TEXT,
	"ssid"	TEXT,
	"encryption"	TEXT,
	"vendor"	TEXT,
	"model"	TEXT,
	"modelnumber"	TEXT,
	"serialnumber"	INTEGER,
	"devicename"	TEXT,
	"primarydevicetype"	TEXT,
	"uuid"	TEXT,
	"fingerprint"	TEXT,
	PRIMARY KEY("id" AUTOINCREMENT)
);
CREATE TABLE IF NOT EXISTS "stations" (
	"id"	INTEGER,
	"ssid"	TEXT,
	"bssid"	TEXT,
	"vendor"	TEXT,
	"fingerprint"	TEXT,
	PRIMARY KEY("id" AUTOINCREMENT)
);
COMMIT;
