import subprocess, re
from termcolor import colored
import asyncio

interface_usable = False

class Capture:
    interface = "wlan0"

    @staticmethod
    async def bring_down():
        subprocess.run(
            f"sudo ip link set {Capture.interface} down",
            shell=True,
            check=False
        )
        await asyncio.sleep(0.4)

    @staticmethod
    async def bring_up():
        subprocess.run(
            f"sudo ip link set {Capture.interface} up",
            shell=True,
            check=False
        )
        await asyncio.sleep(0.4)

    @staticmethod
    async def set_mode_monitor():
        print(colored("[*] Switching to monitor mode...", "yellow"))
        await Capture.bring_down()
        subprocess.run(
            f"sudo iw dev {Capture.interface} set type monitor",
            shell=True,
            check=True
        )
        await Capture.bring_up()
        await asyncio.sleep(0.5)

    @staticmethod
    async def set_mode_managed():
        print(colored("[*] Switching to managed mode...", "yellow"))
        await Capture.bring_down()
        subprocess.run(
            f"sudo iw dev {Capture.interface} set type managed",
            shell=True,
            check=True
        )
        await Capture.bring_up()
        await asyncio.sleep(0.5)

    @staticmethod
    async def get_mode():
        try:
            output = subprocess.check_output(
                f"iw dev {Capture.interface} info | grep type",
                shell=True
            ).decode().strip()
            mode = output.replace("type ", "").strip()
            return mode
        except subprocess.CalledProcessError:
            return None

    @staticmethod
    async def scan():
        
        if await Capture.get_mode() != "managed":
            print(colored("[*] Ensuring card is in managed mode...", "yellow"))
            await Capture.set_mode_monitor()
        # else:
        #     print(colored("[+] Already in managed mode!", "green"))
        
        # print(colored(f"[*] Scanning...", "blue"))

        result = subprocess.check_output(
            f"iw dev {Capture.interface} scan",
            shell=True
        ).decode().strip()

        network_sections = re.split(
            r'(?=^BSS\s[0-9a-f:]{17}\(on wlan0\))', result, flags=re.MULTILINE
        )

        all_networks = []

        for section in network_sections:
            section = section.strip()
            if not section: continue
            
            td = {}

            td["bssid"] = re.search(r'^BSS\s([0-9a-f:]{17})', section, re.MULTILINE)
            td["bssid"] = td["bssid"].group(1) if td["bssid"] else None

            td["ssid"] = re.search(r'^\s*SSID:\s*(.+)', section, re.MULTILINE)
            td["ssid"] = td["ssid"].group(1) if td["ssid"] else None

            td["encryption"] = None
            enc_match = re.search(r'RSN:.*?Authentication suites:\s*(\w+)', section, re.DOTALL)
            if enc_match:
                td["encryption"] = enc_match.group(1)

            td["vendor"] = re.search(r'^\s*\*\s*Manufacturer:\s*(.+)', section, re.MULTILINE)
            td["vendor"] = td["vendor"].group(1) if td["vendor"] else None

            td["model"] = re.search(r'^\s*\*\s*Model:\s*(.+)', section, re.MULTILINE)
            td["model"] = td["model"].group(1) if td["model"] else None

            td["modelnumber"] = re.search(r'^\s*\*\s*Model Number:\s*(.+)', section, re.MULTILINE)
            td["modelnumber"] = td["modelnumber"].group(1) if td["modelnumber"] else None

            td["serialnumber"] = re.search(r'^\s*\*\s*Serial Number:\s*(.+)', section, re.MULTILINE)
            td["serialnumber"] = td["serialnumber"].group(1) if td["serialnumber"] else None

            td["devicename"] = re.search(r'^\s*\*\s*Device name:\s*(.+)', section, re.MULTILINE)
            td["devicename"] = td["devicename"].group(1) if td["devicename"] else None

            td["primarydevicetype"] = re.search(r'^\s*\*\s*Primary Device Type:\s*(.+)', section, re.MULTILINE)
            td["primarydevicetype"] = td["primarydevicetype"].group(1) if td["primarydevicetype"] else None

            td["uuid"] = re.search(r'^\s*\*\s*UUID:\s*(.+)', section, re.MULTILINE)
            td["uuid"] = td["uuid"].group(1) if td["uuid"] else None

            all_networks.append(td)

        return all_networks



