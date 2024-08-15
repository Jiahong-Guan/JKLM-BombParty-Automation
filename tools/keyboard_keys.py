import os
import keyboard
from pprint import pprint
from colorama import init, Fore


init(autoreset=True)
RED = Fore.RED


class KeyboardKeys:
    def __init__(self):
        self.running = True
        self.detect_key_running = True
        self.hook_id = None

    @staticmethod
    def display_all_key_names() -> None:
        print('Display All Key Names:')
        pprint(keyboard._canonical_names.canonical_names)
        input('\n Press "Enter" to continue...')

    @staticmethod
    def display_all_modifiers():
        print('Display All Modifiers:')
        pprint(keyboard.all_modifiers)
        input('\nPress "Enter" to continue...')

    @staticmethod
    def print_key_name(event):
        key_name = event.name
        print(f"Key pressed: {key_name}")

    def detect_key_name_by_press(self):
        keyboard.on_press(self.print_key_name, suppress=True)

        print("Close the program using the mouse to exit.")
        while self.detect_key_running:
            pass

    @staticmethod
    def clear_console():
        os.system('cls')


if __name__ == '__main__':
    keyboard_keys = KeyboardKeys()

    while True:
        keyboard_keys.clear_console()
        print('Keyboard Tool')
        print('Options:')
        print('1. Display all keyboard key names')
        print('2. Display all keyboard modifier names')
        print('3. Detect key name by press (Have to use mouse to exit the program)\n')

        choice = input('>> ').strip()

        if choice.isdigit():
            keyboard_keys.clear_console()
            if choice == '1':
                keyboard_keys.display_all_key_names()
            elif choice == '2':
                keyboard_keys.display_all_modifiers()
            elif choice == '3':
                print(f'{RED}WARNING Your keyboard will not work until you close the program!')
                choice = input('Do you wish to continue? (Y/N) ').lower().strip()

                if choice == 'y':
                    keyboard_keys.clear_console()
                    keyboard_keys.detect_key_name_by_press()
            else:
                print('Invalid Choice')
        else:
            print('Invalid Choice')
