from termcolor import colored
import sys, os, asyncio
from dataclasses import dataclass
from capture import Capture
from fingerprint import Fingerprint
from database import DatabaseConnector

db = DatabaseConnector("database.db").connect()

@dataclass
class Mode:
    key: str
    text: str
    selected: bool = False

MODES = [
    Mode("autofingerprint", "Auto Fingerprint"),
    Mode("autosave", "Auto save to database"),
]

BANNER = r"""
         ,-.
        / \  `.  __..-,O
       :   \ --''_..-'.'
       |    . .-' `. '.
       :     .     .`.'
        \     `.  /  ..
         \      `.   ' .
          `,       `.   \
         ,|,`.        `-.\
        '.||  ``-...__..-`
         |  |
         |__|
         /||\
        //||\
       // || \
    __//__||__\__
   '--------------'

   https://github.com/notvfive/aerotrace
"""

def clear():
    os.system("clear")

def is_mode_enabled(key: str) -> bool:
    for mode in MODES:
        if mode.key == key:
            return mode.selected
    return False

def print_banner():
    print(colored(BANNER, "blue"))

def print_menu(modes: list[Mode]):
    print_banner()
    print(colored("=== Available Modes ===\n", "cyan"))
    
    for i, mode in enumerate(modes, 1):
        print(colored(f"[{i}] {mode.text} ({'ON' if mode.selected else 'OFF'})", "green" if mode.selected else "red"))
    
    print(colored("\n[0] Start", "blue"))
    print(colored("[99] Exit", "yellow"))

def handle_selection(choice: int, modes: list[Mode]):
    if choice == 0:
        print(colored("\nStarting AeroTrace...\n", "blue"))
        return "start"
    
    if choice == 99:
        print(colored("\nGoodbye!\n", "yellow"))
        sys.exit(0)

    if 1 <= choice <= len(modes):
        mode = modes[choice - 1]
        mode.selected = not mode.selected
        print(colored(f"> Toggled {mode.text} to {'ON' if mode.selected else 'OFF'}", "cyan"))
        return "continue"
    
    print(colored("Invalid option.", "red"))
    return "continue"

async def show():
    while True:
        clear()
        print_menu(MODES)

        try:
            choice = int(input(colored("\nSelect an option: ", "white")))
            if handle_selection(choice, MODES) == "start":
                clear()
                while True:
                    try:
                        net_results = await Capture.scan()

                        for network in net_results:
                            bssid = network.get("bssid")
                            ssid = network.get("ssid") or "<hidden>"
                            encryption = network.get("encryption")
                            vendor = network.get("vendor")
                            model = network.get("model")
                            modelnumber = network.get("modelnumber")
                            serialnumber = network.get("serialnumber")
                            devicename = network.get("devicename")
                            primarydevicetype = network.get("primarydevicetype")
                            uuid = network.get("uuid")

                            if not bssid:
                                continue

                            fp = ""
                            if is_mode_enabled("autofingerprint"):
                                try:
                                    fp = await Fingerprint.Generate(network)
                                except Exception as e:
                                    print(colored(f"[!] Fingerprint error for {bssid}: {e}", "red"))

                            if is_mode_enabled("autosave"):
                                try:
                                    exists = await db.is_bssid_already_saved(bssid)
                                    if not exists:
                                        print(colored(f"[*] Saving {ssid} ({bssid}) to database...", "blue"))

                                        await db.execute_query(
                                            """
                                            INSERT INTO accesspoints 
                                            (bssid, ssid, encryption, vendor, model, modelnumber, serialnumber, 
                                            devicename, primarydevicetype, uuid, fingerprint)
                                            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                                            """,
                                            (
                                                bssid,
                                                ssid,
                                                encryption,
                                                vendor,
                                                model,
                                                modelnumber,
                                                serialnumber,
                                                devicename,
                                                primarydevicetype,
                                                uuid,
                                                fp
                                            )
                                        )
                                except Exception as e:
                                    print(colored(f"[!] DB error: {e}", "red"))

                            print(f"{bssid} - {ssid} - {fp}")

                    except Exception as e:
                        print(colored(f"[!] Scan loop error: {e}", "red"))

                    await asyncio.sleep(1)
        except ValueError:
            print(colored("Please enter a number.", "red"))
        except Exception as e:
            print(colored(f"Unexpected error:\n{e}", "red"))
            sys.exit(1)

if __name__ == "__main__":
    if os.name == "nt":
        print(colored("AeroTrace is for linux use only.", "red"))
        sys.exit(1)

    if os.getuid() != 0:
        print(colored("AeroTrace must be ran with sudo.", "red"))
        sys.exit(1)

    asyncio.run(show())
