import asyncio
from database import DatabaseConnector
from fingerprint import Fingerprint
from capture import Capture

async def main():
    result = await Capture.scan()

    for i, net in enumerate(result, 1):
        print(f"--- Network {i} ---")
        for k, v in net.items():
            print(f"{k}: {v}")

        fp = await Fingerprint.Generate(net.items())
        print(fp)
        # print(await Fingerprint.DoesFingerprintExist(fp))
        print()

asyncio.run(main())