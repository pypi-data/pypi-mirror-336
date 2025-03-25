from colorama import init, Fore, Back, Style
from intro_designs import thirty_day_intro_designs
from enum import Enum
import random
import time

init(autoreset=True)

def slow_print(text: str, delay=0.1, newline=False, color="BLUE"):
    """
    Prints the given text with a specified color and delay.

    Args:
        text (str): The text to be printed.
        delay (float): The time in seconds to wait before printing the message.
        newline (bool): Whether to print a newline before the text.
        color (str): The color to print the text in. Defaults to "BLUE".

    If the specified color is not available, it defaults to blue.
    """

    if hasattr(Fore, color.upper()):
        color_code = getattr(Fore, color.upper())
    else:
        color_code = Fore.BLUE
        
    if newline:
        print(f"\n{color_code}{text}")
    else: 
        print(f"{color_code}{text}")
    time.sleep(delay)

def slow_print_header(text: str, delay=0.1):
    """
    Prints a header message in bright white color with blue background and a delay

    Args:
        text (str): The text to be printed as header
        delay (float): The time in seconds to wait before printing the message
    """
    print(f"\n{Fore.WHITE}{Back.BLUE}{Style.BRIGHT}{text}")
    time.sleep(delay)

def slow_print_error(text: str, delay=0.1):
    """
    Prints an error message in red color with a delay

    Args:
        text (str): The text to be printed as error message
        delay (float): The time in seconds to wait before printing the message
    """
    print(f"\n{Fore.RED}⛔️ {text}")
    time.sleep(delay)

def print_intro(day = 1, title = "", subtitle = ""):
    """
    Prints an intro message with a random ASCII art header, day number, 
    title and subtitle. The title and subtitle are padded with spaces 
    to center them in a 28 character wide field.

    Args:
        day (int): The day number to be printed. Defaults to 1.
        title (str): The title to be printed. Defaults to an empty string.
        subtitle (str): The subtitle to be printed. Defaults to an empty string.
    """
    title_padding = (28 - len(title)) // 2
    subtitle_padding = (28 - len(subtitle)) // 2
 
    for row in thirty_day_intro_designs[random.randint(0, len(thirty_day_intro_designs) - 1)]:
        slow_print(row)
    slow_print(f"\n      WELCOME TO DAY {day}!      ")
    slow_print(f"{' ' * title_padding}{title}{' ' * title_padding}")
    slow_print(f"{' ' * subtitle_padding}{subtitle}{' ' * subtitle_padding}")
    slow_print(f"{' ' * 11}***\n")


   