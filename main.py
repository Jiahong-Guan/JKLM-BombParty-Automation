import os
import ast
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

    from playsound import playsound


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

        # Coordinates
        self.top_coordinate: tuple = (698, 567)
        self.bottom_coordinate: tuple = (757, 607)

        # Paths
        self.word_list_path: str = ''
        self.sound_path: str = ''
        self.send_sound_path: str = ''
        self.tesseract_path: str = ''

        self.sfx: bool = False
        self.debug: bool = False

        self.config: ConfigParser = ConfigParser()
        if not os.path.exists('./config.ini'):
            self.create_config_file()
        self.load_config()
        self.load_words()

        print("Press 'Esc' to exit.\n")
        self.play_sound('start')
        keyboard.wait('esc')
        self.play_sound('finish')

    def load_config(self, config_path: str = './config.ini') -> None:
        """
        Load configuration settings from a specified INI file.

        This method reads configuration settings from the provided `config_path` INI file and assigns
        values to the instance's attributes based on the sections and keys defined in the file. The
        configuration is divided into three main sections: 'Settings', 'Path', and 'Coordinates'.
        It also sets up hotkeys based on the configuration.

        Args:
            config_path (str): The path to the INI file to read. Defaults to './config.ini'.

        Returns:
            None

        Attributes:
            self.debug (bool): A boolean indicating whether debug mode is enabled.
            self.sfx (bool): A boolean indicating whether sound effects are enabled.
            self.top_coordinate (tuple): The top coordinate read from the configuration file, evaluated as a tuple.
            self.bottom_coordinate (tuple): The bottom coordinate read from the configuration file, evaluated as a tuple.
            self.word_list_path (str): The file path to the word list.
            self.sound_path (str): The base path for sound files.
            self.send_sound_path (str): The file path for the send sound.
            self.tesseract_path (str): The path to the Tesseract OCR installation.

        Example:
            config_path = './config.ini'
            self.load_config(config_path)
        """
        self.config.read(config_path)

        setting_section = 'Settings'
        path_section = 'Path'
        coordinate_section = 'Coordinates'

        self.debug = self.config.getboolean(setting_section, 'debug')
        self.sfx = self.config.getboolean(setting_section, 'sfx')

        # Coordinates
        top_coordinate = self.config.get(coordinate_section, 'top_coordinate')
        bottom_coordinate = self.config.get(coordinate_section, 'bottom_coordinate')

        self.top_coordinate = ast.literal_eval(top_coordinate)
        self.bottom_coordinate = ast.literal_eval(bottom_coordinate)

        # Paths
        self.word_list_path = self.config.get(path_section, 'word_list_path')
        self.sound_path = self.config.get(path_section, 'base_sound_path')
        self.send_sound_path = self.config.get(path_section, 'send_path')
        self.tesseract_path = self.config.get(path_section, 'pytesseract_path')

        # Assign Hotkey
        self.add_hotkey(self.config.get(setting_section, 'run_key'), self.on_run_key)
        self.add_hotkey(self.config.get(setting_section, 'clear_key'), self.on_clear_key)

    def load_words(self) -> None:
        """
        Loads a list of words from a file specified by the instance's
        `word_list_path` attribute and stores it in the instance's
        `word_list` attribute.

        The method opens the file in read mode, reads each line,
        strips any leading or trailing whitespace from each word, and
        then assigns the list of cleaned words to `self.word_list`.

        This method does not return any value.

        Raises:
            FileNotFoundError: If the file specified by `word_list_path` does not exist.
            IOError: If there is an error reading the file.
        """
        with open(self.word_list_path, 'r') as file:
            self.word_list = [word.strip() for word in file.readlines()]

    @staticmethod
    def add_hotkey(hotkey: str, func: Callable) -> None:
        """
        Registers a global hotkey to trigger a specified function when pressed.

        Args:
           hotkey (str): The key combination to be used as a hotkey.
                         This should be a string representing the key or keys,
                         such as 'ctrl+shift+s' or 'f5'.
           func (Callable): The function to be executed when the hotkey is pressed.
                            This should be a callable object (e.g., a function or a method).

        Returns:
           None

        Example:
           >>> def my_function():
           >>>     print("Hotkey pressed!")
           >>> JKLM_BombPartyAutomation.add_hotkey('ctrl+shift+h', my_function)
        """
        keyboard.add_hotkey(hotkey, func)

    def on_run_key(self) -> None:
        """
        Handles the event triggered when the run key is pressed.

        This method prints a message indicating that a word check is in progress
        and then calls the `run` method to perform the necessary actions.

        Returns:
            None
        """
        self.color_print('Checking for word...', YELLOW)
        self.run()

    def on_clear_key(self) -> None:
        """
        Clears the `used_list` and prints a confirmation message.

        This method empties the `used_list` attribute and outputs a message
        indicating that the list has been cleared. The message is printed
        using the `color_print` method with the color specified as GREEN.

        Returns:
           None: This method does not return any value.
        """
        self.used_list.clear()
        self.color_print('Cleared used list!', GREEN)

    def play_sound(self, sound_type: Literal["start", "finish", "send"]) -> None:
        """
        Plays a sound based on the specified sound type.

        Args:
            sound_type (Literal["start", "finish", "send"]): The type of sound to play.
                - "start": Plays the start sound.
                - "finish": Plays the finish sound.
                - "send": Plays a random send sound from a specified range.

        Returns:
            None

        Raises:
            ValueError: If `sound_type` is not one of the specified literals ("start", "finish", "send").

        Notes:
            - Ensure that `self.sfx` is set to True to enable sound playback.
            - The sound files should be located at `self.sound_path` for "start" and "finish" sounds.
            - For "send" sounds, files should be located at `self.send_sound_path`, with filenames corresponding to numbers from 1 to 14.

        Example:
            >>> JKLM_BombPartyAutomation.play_sound("start")
            Plays the start sound.

            >>> JKLM_BombPartyAutomation.play_sound("send")
            Plays a random send sound from the range.
        """
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
        """
        Prints a message in the specified color.

        Args:
            message (str): The message to be printed.
            color (str): The color code or color name to format the message. This is
                         typically an ANSI escape code or a color name supported by the
                         terminal or output environment.

        Returns:
            None: This method does not return any value.

        Example:
            >>> JKLM_BombPartyAutomation.color_print("Hello, World!", "\033[92m")
            Hello, World! (printed in green)

        Notes:
            - Ensure that the color code or name is supported by the terminal or environment
              where this function is being used.
            - The color code should be in the format recognized by the terminal (e.g., ANSI escape codes).
        """
        print(f"{color}{message}")

    @staticmethod
    def create_config_file() -> None:
        """
        Creates a default `config.ini` configuration file with predefined sections and settings.

        This method generates a configuration file named `config.ini` with the following sections:

        - **Settings**: Contains application settings such as debug mode and key bindings.
            - `debug` (str): Debug mode flag, set to `'false'` by default.
            - `run_key` (str): Key used to trigger the run action, set to `'page down'` by default.
            - `clear_key` (str): Key used to clear the action, set to `'page up'` by default.
            - `sfx` (str): Sound effects flag, set to `'true'` by default.

        - **Coordinates**: Contains coordinate settings used by the application.
            - `top_coordinate` (str): The top coordinate in the format `(x, y)`, default is `'(698, 567)'`.
            - `bottom_coordinate` (str): The bottom coordinate in the format `(x, y)`, default is `'(757, 607)'`.

        - **Path**: Contains file paths used by the application.
            - `word_list_path` (str): Path to the word list file, default is `'./word_list/words.txt'`.
            - `base_sound_path` (str): Base path for sound files, default is `'./sound'`.
            - `send_path` (str): Path for the send sound files, default is `'./sound/send'`.
            - `pytesseract_path` (str): Path to the Tesseract OCR executable, default is `r'C:\Program Files\Tesseract-OCR\tesseract.exe'`.

        Returns:
            None: This method does not return any value.

        Notes:
            - The `config.ini` file will be created in the current working directory.
            - Paths and coordinates are set to default values; adjust as needed for your environment.
        """
        config = ConfigParser()

        # Settings Section
        config['Settings'] = {
            'debug': 'false',
            'run_key': 'page down',
            'clear_key': 'page up',
            'sfx': 'true'
        }

        # Coordinates Section
        config['Coordinates'] = {
            'top_coordinate': '(698, 567)',
            'bottom_coordinate': '(757, 607)'
        }

        # Path Section
        config['Path'] = {
            'word_list_path': './word_list/words.txt',
            'base_sound_path': './sound',
            'send_path': './sound/send',
            'pytesseract_path': r'C:\Program Files\Tesseract-OCR\tesseract.exe'
        }

        # Write the configuration file
        with open('config.ini', 'w') as configfile:
            config.write(configfile)

    def run(self) -> None:
        """
        Shuffles the `word_list` and processes a sequence of words to find and handle a match.

        The method performs the following steps:
        1. Shuffles the `word_list` in place.
        2. Retrieves a sequence of characters and converts it to lowercase.
        3. Searches for a word in the `word_list` that matches the given sequence.
        4. If debugging is enabled, prints the sequence to the console.
        5. If a matching word is found, performs the following actions:
           - Prints the found word.
           - Clears the current text input using 'Ctrl+A' and 'Backspace'.
           - Types the found word and presses 'Enter'.
           - Plays a sound to indicate the word has been sent.
           - Appends the found word to the `used_list`.

        This method relies on external libraries such as `pyautogui` for keyboard actions and `self.play_sound` for sound notifications.
        """
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
        """
        Find and return the first word from `self.word_list` that contains the specified sequence
        and is not already in `self.used_list`.

        Args:
            sequence (str): The sequence of characters to search for within the words of `self.word_list`.

        Returns:
            str: The first word that contains the sequence and is not in `self.used_list`.
                 If no such word is found, returns an empty string.

        Example:
            >>> JKLM_BombPartyAutomation.find_word_with_sequence('abc')
            'example_word'
            >>> JKLM_BombPartyAutomation.find_word_with_sequence('xyz')
            ''
        """
        # return [word for word in self.word_list if sequence in word and word not in self.used_list]
        for word in self.word_list:
            if sequence in word and word not in self.used_list:
                return word
        else:
            return ''

    def get_sequence(self) -> str:
        """
        Captures a screenshot of a specified region of the screen, preprocesses the image for OCR (Optical Character Recognition),
        and extracts text from the image.

        This method performs the following steps:
        1. Takes a screenshot of a region defined by the top-left and bottom-right coordinates.
        2. Converts the screenshot to a format suitable for processing.
        3. Preprocesses the image by converting it to grayscale, applying median blur, thresholding, and resizing.
        4. Optionally saves the raw and preprocessed images for debugging purposes.
        5. Uses Tesseract OCR to extract text from the preprocessed image, with custom configuration settings.
        6. Cleans up the extracted text by removing specific characters and returns it in lowercase, trimmed format.

        Returns:
            str: The extracted text from the screenshot, converted to lowercase and stripped of leading/trailing whitespace.

        Note:
            - Ensure Tesseract OCR is properly installed and the path is set in `self.tesseract_path`.
            - Debug images will be saved if `self.debug` is True.
        """
        pytesseract.pytesseract.tesseract_cmd = self.tesseract_path

        # Box Coordinates
        top_left = self.top_coordinate
        bottom_right = self.bottom_coordinate

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
