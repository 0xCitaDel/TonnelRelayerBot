import time

from selenium.webdriver.common.by import By

from src.utils.new_elements_tracker import NewElementsTracker
from src.utils.console import Console
from src.webdriver.browser_manager import BrowserManager
from src.webdriver.local_storage_manager import LocalStorageManager
from src.webdriver.page_elements import PageElements
from src.webdriver.page_parser import TonnelRelayerParser


class BotActions:

    def __init__(
        self, browser: BrowserManager, local_storage: LocalStorageManager,
        interactor: PageElements, parser: TonnelRelayerParser, tracker: NewElementsTracker,
    ) -> None:

        self.browser: BrowserManager = browser
        self.local_storage: LocalStorageManager = local_storage
        self.interactor: PageElements = interactor
        self.parser: TonnelRelayerParser = parser
        self.tracker: NewElementsTracker = tracker
        self.console = Console()

    def _initialization(self):
        START_PAGE_URL = 'https://web.telegram.org/a/'
        START_PAGE_LOADED_CHECK = '.qr-container'

        self.browser.open_page(START_PAGE_URL, START_PAGE_LOADED_CHECK)

        self.local_storage.load_local_storage()

        self.browser.refresh_page()

        self.interactor.force_click_element(By.XPATH, "//a[@href='#6013927118']")
        self.interactor.force_click_element(By.CSS_SELECTOR, ".bot-menu-text")
        time.sleep(5)
        self.interactor.force_click_element(
            By.XPATH, '//*[@id="portals"]/div[2]/div/div/div[2]/div[2]/div/button[1]'
        )

        time.sleep(5)

    def run(self):

        self._initialization()
        self.browser.driver.switch_to.frame(0)

        while True:
            self.interactor.force_click_element(
                By.XPATH, '//*[@id="root"]/div/div[4]/div/div/a[2]'
            )
            time.sleep(2)
            self.interactor.force_click_element(
                By.XPATH, '//*[@id="root"]/div/div[4]/div/div/a[1]'
            )
            time.sleep(4)
            nfts = self.parser.check_by_name_and_price()
            new_items = self.tracker.check_new(nfts)

            if not new_items:
                print("No new items")
            else:
                print('---------------- NEW_ITEMS ---------------- ')
                for i in new_items:
                    print(f'{i['name']} - {i['model']}: {i['price']} TON')
            time.sleep(2)
