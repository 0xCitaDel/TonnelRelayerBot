from typing import Callable, ContextManager

from selenium.common.exceptions import (ElementClickInterceptedException,
                                        NoSuchElementException,
                                        TimeoutException)
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from src.logs.task_progress import TaskProgressManager


class Actions:

    def __init__(
        self,
        driver,
        task: Callable[[str], ContextManager[TaskProgressManager]],
    ) -> None:
        self.driver = driver

        self.task = task

    def find_element(self, by: str, value: str, time=10):
        with self.task(f"Try to find element: {value}") as t:
            try:
                return WebDriverWait(self.driver, time).until(
                    EC.presence_of_element_located((by, value))
                )
            except (TimeoutException, NoSuchElementException) as e:
                t.complete_task(desc=f"⚠️ Not found element: {value} ({e})", status="error")
                return None

    def click_element(self, by, value: str):
        with self.task(f"Try to click: {value}") as t:
            element = self.find_element(by, value)

            if element is None:
                return False

            try:
                WebDriverWait(self.driver, 10).until(
                    EC.element_to_be_clickable((by, value))
                )
                element.click()
                t.complete_task()
                return True

            except ElementClickInterceptedException:
                t.complete_task(desc=f"Click blocked: {value}", status='error')
            except Exception as e:
                t.complete_task(desc=f"Click error: {value} ({e})", status='error')

            return False

    def force_click_element(self, by, value):
        with self.task('Force clik') as t:
            while True:
                if self.click_element(by, value):
                    t.complete_task()
                    break
                else:
                    self.driver.refresh_page()
                    t.complete_task(desc="Click failed. Retrying", status='warning')
