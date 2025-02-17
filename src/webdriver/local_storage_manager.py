import json
import sys

from src.logger_config import log


class LocalStorageManager:
    """Manages the browser's local storage"""

    def __init__(self, driver, local_storage_path):
        """
        Initializes the LocalStorageManager.

        :param driver: WebDriver instance
        :param local_storage_path: Path to the local storage JSON file
        """

        self.driver = driver
        self.local_storage_path = local_storage_path

    def load_local_storage(self):
        """Loads data into localStorage from a JSON file."""
        try:
            log.info("Loading local storage...")
            with open(self.local_storage_path, "r", encoding="utf-8") as file:
                data = json.load(file)

                for key, value in data.items():
                    self._add_local_storage_item(key, value)

            log.info("Local storage updated.")

        except json.JSONDecodeError:
            log.error("JSON file is not formatted correctly.")
            sys.exit(1)

        except FileNotFoundError:
            log.error(f"Local storage file not found: {self.local_storage_path}")
            sys.exit(1)

        except Exception as e:
            log.error(f"Storage error: {e}")
            sys.exit(1)


    def _add_local_storage_item(self, key, value):
        """
        Adds a key-value pair to localStorage.

        :param key: The key to store
        :param value: The value associated with the key
        """
        self.driver.execute_script(f"window.localStorage.setItem('{key}', '{value}');")
