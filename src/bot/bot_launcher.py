import time

from selenium.webdriver.common.by import By

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
            driver=self.browser.driver,
            local_storage_path=LOCAL_STORAGE_JSON_PATH
        )
        self.actions = Actions(driver=self.browser.driver)
        self.parser = TonnelRelayerParser(driver=self.browser.driver, config_path=CONFIG_PATH)

        # Temp decision
        self.tracker: NewElementsTracker = NewElementsTracker()

    def run(self):
        try:
            self.initialization()
        except Exception as e:
            log.exception(f"Unexpected error: {e}")
        finally:
            self.browser.close_browser()

    def initialization(self):
        START_PAGE_URL = 'https://web.telegram.org/a/'
        START_PAGE_LOADED_CHECK = '.qr-container'

        with self.task('Open browser') as t:
            self.browser.open_page(START_PAGE_URL, START_PAGE_LOADED_CHECK)

        self.local_storage.load_local_storage()

        self.browser.refresh_page()
        time.sleep(1000)

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
            time.sleep(2)
            nfts = self.parser.check_by_name_and_price()
            new_items = self.tracker.check_new(nfts)

            if not new_items:
                print("No new items")
            else:
                print('---------------- NEW_ITEMS ---------------- ')
                for i in new_items:
                    print(f'{i['name']} - {i['model']}: {i['price']} TON')
            time.sleep(2)
