# 1. Add to Browser Chrome
# https://chromewebstore.google.com/detail/manage-localstorage/hjbkmghihndbbjggaiocmlihachebmcn
# 2. Press "Export" -> "Copy" -> Paste into local_storage.json file"

from src.constants import DRIVER_PATH, LOCAL_STORAGE_JSON_PATH, CONFIG_PATH
from src.logger_config import log
from src.webdriver.actions import BotActions
from src.webdriver.page_parser import TonnelRelayerParser
from src.webdriver.browser_manager import BrowserManager
from src.webdriver.local_storage_manager import LocalStorageManager
from src.webdriver.page_elements import PageElements
from src.utils.new_elements_tracker import NewElementsTracker


def main():
    browser = BrowserManager(DRIVER_PATH)
    interactor = PageElements(browser.driver)
    storage_manager = LocalStorageManager(browser.driver, LOCAL_STORAGE_JSON_PATH)
    parser = TonnelRelayerParser(browser.driver, CONFIG_PATH)
    tracker = NewElementsTracker()

    bot = BotActions(browser, storage_manager, interactor, parser, tracker)

    try:
        bot.run()
    except Exception as e:
        log.error(f"❌ Unexpected error: {e}")
    finally:
        browser.close_browser()


if __name__ == "__main__":
    main()
