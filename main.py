from termcolor import colored
import sys, os
from dataclasses import dataclass

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
"""

def clear():
    if os.name == "nt":
        os.system("cls")
    else:
        os.system("clear")

def print_banner():
    print(BANNER)

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

def show():
    while True:
        clear()
        print_menu(MODES)

        try:
            choice = int(input(colored("\nSelect an option: ", "white")))
            if handle_selection(choice, MODES) == "start":
                break

        except ValueError:
            print(colored("Please enter a number.", "red"))

        except Exception as e:
            print(colored(f"Unexpected error:\n{e}", "red"))
            sys.exit(1)

if __name__ == "__main__":
    show()
