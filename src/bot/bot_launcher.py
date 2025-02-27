import time

from selenium.webdriver.common.by import By

from src.bot.http_client import http_coffin
from src.browser.actions import Actions
from src.browser.browser_manager import BrowserManager
from src.browser.local_storage import LocalStorageManager
from src.browser.parser import TonnelRelayerParser
from src.constants import CONFIG_PATH, DRIVER_PATH, LOCAL_STORAGE_JSON_PATH
from src.logs.log import log
from src.logs.progress import ProgressManager
from src.utils.new_elements_tracker import NewElementsTracker


class BotLauncher(ProgressManager):
    def __init__(self, task_disable: bool):
        super().__init__(task_disable)
        self.browser = BrowserManager(driver_path=DRIVER_PATH)
        self.local_storage = LocalStorageManager(
            driver=self.browser.driver, local_storage_path=LOCAL_STORAGE_JSON_PATH
        )
        self.actions = Actions(driver=self.browser.driver)

        # Temp decision
        self.tracker: NewElementsTracker = NewElementsTracker()

        self.parser = TonnelRelayerParser(
            driver=self.browser.driver, filters_path=CONFIG_PATH, tracker=self.tracker
        )

    def run(self):
        try:
            self.initialization()
        except Exception as e:
            log.exception(f"Unexpected error: {e}")
        finally:
            self.browser.close_browser()

    def initialization(self):
        START_PAGE_URL = "https://web.telegram.org/a/"
        START_PAGE_LOADED_CHECK = ".qr-container"

        with self.task("Open browser"):
            self.browser.open_page(START_PAGE_URL, START_PAGE_LOADED_CHECK)

        self.local_storage.load_local_storage()

        self.browser.refresh_page()

        self.actions.force_click_element(By.XPATH, "//a[@href='#6013927118']")
        self.actions.force_click_element(By.CSS_SELECTOR, ".bot-menu-text")
        time.sleep(5)
        self.actions.force_click_element(
            By.XPATH, '//*[@id="portals"]/div[2]/div/div/div[2]/div[2]/div/button[1]'
        )

        time.sleep(5)

        self.browser.driver.switch_to.frame(0)

        while True:
            self.actions.force_click_element(
                By.XPATH, '//*[@id="root"]/div/div[4]/div/div/a[2]'
            )
            time.sleep(2)
            self.actions.force_click_element(
                By.XPATH, '//*[@id="root"]/div/div[4]/div/div/a[1]'
            )
            time.sleep(1)

            filtered_nfts = self.parser.filter_by_config()

            for gift in filtered_nfts:
                auth_data = self.parser.get_balance_info["authData"]
                respone = http_coffin.buy_gift(
                    auth_data, gift_id=gift["gift_id"], price=gift["price"]
                )
                print(respone)
                time.sleep(1000)

            time.sleep(100)
