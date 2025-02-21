import json
import sys
from typing import Callable, ContextManager

from src.logs.task_progress import TaskProgressManager


class LocalStorageManager:
    """Manages the browser's local storage"""

    def __init__(
        self,
        driver,
        task: Callable[[str], ContextManager[TaskProgressManager]],
        local_storage_path,
    ):
        """
        Initializes the LocalStorageManager.

        :param driver: WebDriver instance
        :param local_storage_path: Path to the local storage JSON file
        """

        super().__init__()
        self.driver = driver
        self.local_storage_path = local_storage_path

        self.task = task

    def load_local_storage(self):
        """Loads data into localStorage from a JSON file."""
        with self.task("Try to loading local storage") as t:
            try:
                with open(self.local_storage_path, "r", encoding="utf-8") as file:
                    data = json.load(file)

                    for key, value in data.items():
                        self._add_local_storage_item(key, value)

                t.complete_task()

            except json.JSONDecodeError:
                t.complete_task(
                    desc="JSON file is not formatted correctly", status="error"
                )
                sys.exit(1)

            except FileNotFoundError:
                t.complete_task(
                    desc=f"local storage file not found: {self.local_storage_path}",
                    status="error",
                )
                sys.exit(1)

            except Exception as e:
                t.complete_task(desc=f"Storage error: {e}", status="error")
                sys.exit(1)

    def _add_local_storage_item(self, key, value):
        """
        Adds a key-value pair to localStorage.

        :param key: The key to store
        :param value: The value associated with the key
        """
        self.driver.execute_script(f"window.localStorage.setItem('{key}', '{value}');")
