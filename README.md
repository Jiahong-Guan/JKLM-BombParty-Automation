# JKLM Bomb Party Automation

---

This Python script automates certain tasks in the JKLM game "Bomb Party."

It utilizes OCR (Optical Character Recognition) to detect sequences of letters in the game, searches for a matching word from a predefined list, and automatically inputs it. 

The script also includes sound effects and supports customizable hotkeys.


### <font color="red"> IMPORTANT LIMITATION OF OCR </font>

- The OCR (pyTesseract) may sometimes misinterpret uppercase `I` as lowercase `L`. When this happens, you will need to manually type out the correct word according to the sequence yourself.
- Occasionally, JKLM might report the word as invalid. If this occurs, simply press the Run Key repeatedly until a valid word is accepted.


## Features

---

- **OCR Detection**: Captures a portion of the screen to detect sequences of letters.
- **Word Matching**: Searches for words in a predefined list that match the detected sequence.
- **Automated Input**: Automatically inputs the found word into the game.
- **Sound Effects**: Optional sound effects can be played during the automation process.
- **Customizable Hotkeys**: Configure hotkeys to start the automation or clear the used word list.


## Requirements

---

- Python 3.6+
- The following Python libraries:
  - `os`
  - `sys`
  - `cv2` (OpenCV)
  - `random`
  - `keyboard`
  - `pyautogui`
  - `subprocess`
  - `pytesseract`
  - `numpy`
  - `colorama`
  - `configparser`
  - `playsound`


## Installation

---

1. Install [Tesseract installer for Windows](https://github.com/UB-Mannheim/tesseract/releases/download/v5.4.0.20240606/tesseract-ocr-w64-setup-5.4.0.20240606.exe)
and set the installation path to `C:\Program Files\Tesseract-OCR\`.

2. Clone the repository or download the script.
3. Install the required Python libraries using pip:
   ```bash
   pip install -r requirements.txt
   ```


## Hotkeys

---

- **Run Key** (Default: `Page Down`): Starts the OCR detection and word matching process.
- **Clear Key** (Default: `Page Up`): Clears the list of used words. (Use this when a new round starts)

You can customize these hotkeys in the [config.ini](config.ini) file. 
Refer to [Hotkey Configuration](#hotkey-configuration) for more information. 


## Usage

---

1. Make sure that the config.ini file is properly configured with the correct paths for word list, sound files, and Tesseract OCR.
2. Run the script:
    ```bash
    python main.py
    ```
3. To exit the program, press `Esc` key.

The automation will start, and you can control it using the configured hotkeys.


## Configuration

---

### Coordinates Configuration

- The current window resolution is set to `1920 x 1080`. It is recommended to use this resolution for optimal performance. If you need to change the resolution, you must adjust the coordinates of the detection box accordingly.
  
  To determine the correct coordinates for the detection box, use the [mouse_position.py](tools/mouse_position.py) script located in the [tools](tools) directory. Refer to the [image](examples/screenshot.png) for guidance on which region to select.

  **Usage for `mouse_position.py`:**
  - Run the file and left-click on any position on the screen to obtain the coordinates.

  After capturing the coordinates for both the top-left and bottom-right corners of the box, set these as a tuple in the [config.ini](config.ini) file under the `Coordinates` section.


### Hotkey Configuration

- The script uses the `keyboard` library to register hotkeys. You can customize the hotkey bindings by modifying the [config.ini](config.ini) file.

- To view available key names and modifiers, or to detect key presses for custom keybinds, use the `keyboard_keys.py` script located in the [tools](tools) directory.

  **Usage for `keyboard_keys.py`:**
  1. Run the script:
     ```bash
     python tools/keyboard_keys.py
     ```
  2. You will see a menu with the following options:
     - **Display all keyboard key names**: Lists all possible key names you can use.
     - **Display all keyboard modifier names**: Lists all available modifier keys (e.g., Shift, Ctrl).
     - **Detect key name by press**: Allows you to detect the name of a key by pressing it. Note that your keyboard input will be disabled while this mode is active, and you will need to use the mouse to close the program.

  **Example:**
  If you want to set the Run Key to a combination of `Ctrl` + `Alt` + `F12`, find the key names in the list displayed by the script and update the `config.ini` file as follows:
  ```ini
  [Settings]
  run_key = ctrl+alt+f12
  ```
  Similarly, to change the Clear Key to a combination of Ctrl + Shift + F11, find its name and update:
  ```ini
  [Settings]
  clear_key = ctrl+shift+f11
  ```
  
- After updating the `config.ini` file with your desired keybindings, save the changes and restart the script for the new hotkey configurations to take effect.

### Explanation:

- **Example of Combining Multiple Keys**: Provides specific examples of how to configure complex key combinations in the `config.ini` file.
- **Instruction for Multiple Keys**: Shows how to use the `+` sign to combine multiple keys (e.g., `ctrl+alt+f12`).

This update ensures users know how to set both single and multiple key combinations for their hotkeys.

**NOTE:** Try not to use common keybindings that websites usually use like `ctrl+r`.

## Troubleshooting

---

- If OCR (pyTesseract) is not detecting the word sequence, ensure that your display resolution is `1920 x 1080` but if it is not please refer to [Coordinates Configuration](#coordinates-configuration) to adjust the coordinate of where OCR captures.
- Ensure Tesseract OCR is installed and the correct path is provided in config.ini.
- If sound doesn't play, verify the sound file paths in the configuration.


## Acknowledgments

---

- **Tesseract OCR:** For the text recognition engine.
- **Colorama:** For terminal text coloring.
- **Playsound:** For simple sound playback.


## License

---

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
