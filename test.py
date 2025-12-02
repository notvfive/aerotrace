from database import DatabaseConnector
from fingerprint import Fingerprint
from capture import Capture

result = Capture.scan()
for i, net in enumerate(result, 1):
    print(f"--- Network {i} ---")
    for k,v in net.items():
        print(f"{k}: {v}")

    fp = Fingerprint.Generate(net.items())
    print(fp)
    print(Fingerprint.DoesFingerprintExist(fp))
    print()