from typing import Callable, ContextManager

from selenium.common.exceptions import TimeoutException
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from seleniumwire import webdriver

from src.logs.task_progress import TaskProgressManager


class BrowserManager:

    def __init__(
        self,
        driver_path,
        task: Callable[[str], ContextManager[TaskProgressManager]],
        max_retries=3,
    ):
        """
        :param local_storage_path: Path to local storage JSON file
        :param max_retries: Max retries if the page fails to load
        """
        super().__init__()
        self.service = Service(executable_path=driver_path)
        self.options = webdriver.ChromeOptions()
        self.options.set_capability("goog:loggingPrefs", {"performance": "ALL"})

        self.driver = webdriver.Chrome(service=self.service, options=self.options)
        self.driver.execute_cdp_cmd("Network.enable", {})

        self.max_retries = max_retries

        self.task = task

    def open_page(self, url, check_element, by=By.CSS_SELECTOR):
        with self.task(f"Try to open: {url}") as t:
            self.driver.get(url)

            if not self._retry_until_loaded(by, check_element):
                t.complete_task("Page failed to load. Exiting.", status="error")
                self.close_browser()

                raise Exception("Page load error.")

    def refresh_page(self):
        with self.task("Try to refresh page"):
            self.driver.refresh()

    def close_browser(self):
        with self.task("Try to close browser"):
            self.driver.quit()

    def _retry_until_loaded(self, by, value):  # [TODO] Change method name
        """Reload until the page loads successfully."""
        with self.task("Try to reload page") as t:
            for attempt in range(self.max_retries):
                t.complete_task(
                    desc=f"🔄 Checking page load ({attempt + 1}/{self.max_retries})...",
                    status="info",
                )

                if self._is_element_present(by, value):
                    return True

                t.complete_task(desc="Reloading page...", status="warning")

                self.driver.refresh()

            t.complete_task(
                desc="❌ Page failed to load after retries.", status="error"
            )

            return False

    def _is_element_present(self, by, value, timeout=10):
        """Checks whether the item has been loaded in the specified time."""
        with self.task(f'Try to find: {value}') as t:
            try:
                WebDriverWait(self.driver, timeout).until(
                    EC.presence_of_element_located((by, value))
                )
                t.complete_task(status='succeed')
                return True

            except TimeoutException:
                t.complete_task(desc=f"⚠️ Element not found: {value} (Waited {timeout}s)", status='error')
                return False
