import os
import sys
import cv2
import random
import keyboard
import pyautogui
import subprocess
import pytesseract
import numpy as np

from typing import Callable, Literal
from configparser import ConfigParser
from colorama import init, Fore

try:
    from playsound import playsound
except ModuleNotFoundError:
    if os.path.basename(__file__).split('.')[1] == 'py':
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', '--upgrade', 'pip'])
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', '--only-binary=:all:', 'playsound~=1.2.2'])


# Initialize Colorma
init(autoreset=True)
RED = Fore.RED
YELLOW = Fore.YELLOW
GREEN = Fore.GREEN


class JKLM_BombPartyAutomation:
    def __init__(self) -> None:
        self.used_list: list = []
        self.sequence: str = ""
        self.word_list: list = []

        # Paths
        self.word_list_path: str = ''
        self.sound_path: str = ''
        self.send_sound_path: str = ''
        self.tesseract_path: str = ''

        self.sfx: bool = False
        self.debug: bool = False

        self.config: ConfigParser = ConfigParser()
        self.load_config()
        self.load_words()

        print("Press 'Esc' to exit.\n")
        self.play_sound('start')
        keyboard.wait('esc')
        self.play_sound('finish')

    def load_config(self, config_path: str = './config.ini') -> None:
        self.config.read(config_path)

        setting_section = 'Settings'
        path_section = 'Path'

        self.debug = self.config.getboolean(setting_section, 'debug')
        self.sfx = self.config.getboolean(setting_section, 'sfx')

        self.word_list_path = self.config.get(path_section, 'word_list_path')
        self.sound_path = self.config.get(path_section, 'base_sound_path')
        self.send_sound_path = self.config.get(path_section, 'send_path')
        self.tesseract_path = self.config.get(path_section, 'pytesseract_path')

        self.add_hotkey(self.config.get(setting_section, 'run_key'), self.on_run_key)
        self.add_hotkey(self.config.get(setting_section, 'clear_key'), self.on_clear_key)

    def load_words(self) -> None:
        with open(self.word_list_path, 'r') as file:
            self.word_list = [word.strip() for word in file.readlines()]

    @staticmethod
    def add_hotkey(hotkey: str, func: Callable) -> None:
        keyboard.add_hotkey(hotkey, func)

    def on_run_key(self) -> None:
        self.color_print('Checking for word...', YELLOW)
        self.run()

    def on_clear_key(self) -> None:
        self.used_list.clear()
        self.color_print('Cleared used list!', GREEN)

    def play_sound(self, sound_type: Literal["start", "finish", "send"]) -> None:
        if self.sfx:
            if sound_type == 'start':
                playsound(f'{self.sound_path}/start.mp3')
            elif sound_type == 'finish':
                playsound(f'{self.sound_path}/finish.mp3')
            elif sound_type == 'send':
                random_number = random.randint(1, 14)
                playsound(f'{self.send_sound_path}/{random_number}.mp3')
            else:
                self.color_print(f'Sound type is invalid: {sound_type}', RED)

    @staticmethod
    def color_print(message: str, color: str) -> None:
        print(f"{color}{message}")

    def create_config_file(self):  # TODO:
        pass

    def run(self) -> None:
        random.shuffle(self.word_list)

        self.sequence = self.get_sequence().lower()
        found_word = self.find_word_with_sequence(self.sequence)

        if self.debug:
            print(f'Sequence:   {self.sequence}')

        if found_word != '':
            print(f'Found word: {found_word}')
            pyautogui.hotkey('ctrl', 'a')
            pyautogui.press('backspace')
            pyautogui.write(found_word)
            pyautogui.press('enter')
            self.play_sound('send')
            self.used_list.append(found_word)

    def find_word_with_sequence(self, sequence) -> str:
        # return [word for word in self.word_list if sequence in word and word not in self.used_list]
        for word in self.word_list:
            if sequence in word and word not in self.used_list:
                return word
        else:
            return ''

    def get_sequence(self) -> str:
        pytesseract.pytesseract.tesseract_cmd = self.tesseract_path

        # Box Coordinates
        top_left = (698, 567)
        bottom_right = (757, 607)

        left = top_left[0]
        top = top_left[1]
        region_width = bottom_right[0] - left
        region_height = bottom_right[1] - top
        region = (left, top, region_width, region_height)

        # Take a screenshot of the specified region
        screenshot = pyautogui.screenshot(region=region)
        if self.debug:
            screenshot.save('screenshot_raw.png')

        # Convert the screenshot to a numpy array for processing
        screenshot = np.array(screenshot)

        # Convert the screenshot to a numpy array for processing
        screenshot = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)

        # Preprocess the image to improve OCR accuracy
        gray = cv2.cvtColor(screenshot, cv2.COLOR_BGR2GRAY)  # Convert to grayscale
        gray = cv2.medianBlur(gray, 3)  # Apply median blur to reduce noise
        _, thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)  # Apply thresholding
        thresh = cv2.resize(thresh, None, fx=2, fy=2, interpolation=cv2.INTER_LINEAR)  # Resize to make text clearer

        # Optionally save the preprocessed image for inspection
        if self.debug:
            cv2.imwrite('preprocessed_screenshot.png', thresh)

        # Extract text from the image
        custom_config = r'--oem 3 --psm 6'
        text = pytesseract.image_to_string(thresh, config=custom_config).translate(str.maketrans('', '', '-=>/<|—'))

        return text.lower().strip()


if __name__ == '__main__':
    jklm_bomb_party_automation = JKLM_BombPartyAutomation()
