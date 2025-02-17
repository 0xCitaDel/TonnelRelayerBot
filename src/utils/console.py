import os
import shutil
import sys
import time

from colorama import Fore, Style
from tabulate import tabulate
from tqdm import tqdm


class Console:

    def __init__(self) -> None:
        self.clear_screen()

    @staticmethod
    def spinner(message, duration=3):
        """Анимация загрузки"""
        steps = ["⠋", "⠙", "⠹", "⠸", "⠼", "⠴", "⠦", "⠧", "⠇", "⠏"]
        for _ in range(duration * 4):
            sys.stdout.write(
                f"\r{Fore.YELLOW}{steps[_ % len(steps)]} {message}{Style.RESET_ALL}"
            )
            sys.stdout.flush()
            time.sleep(0.25)
        print("\r✅ " + message + " завершено!")

    def clear_screen(self):
        os.system("cls" if os.name == "nt" else "clear")
