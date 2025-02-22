# from selenium import webdriver
# import seleniumwire.undetected_chromedriver as webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from seleniumwire import webdriver

from src.logs.log import log


class BrowserManager:

    def __init__(
        self,
        driver_path,
    ):
        """
        :param local_storage_path: Path to local storage JSON file
        """
        super().__init__()
        self.service = Service(executable_path=driver_path)

        self.options = webdriver.ChromeOptions()
        self.options.set_capability("goog:loggingPrefs", {"performance": "ALL"})

        self.proxy_options = {
            "proxy": {
                "http": "http://127.0.0.1:8080",
                "https": "https://127.0.0.1:8080",
                "no_proxy": "localhost,127.0.0.1",
            }
        }

        self.driver = webdriver.Chrome(
            service=self.service,
            options=self.options,
            seleniumwire_options=self.proxy_options,
        )
        self.driver.execute_cdp_cmd("Network.enable", {})
        self.driver.request_interceptor = self.modify_headers

    def modify_headers(self, request):
        if request.url == "https://gifts2.tonnel.network":
            request.headers["Host"] = "gifts2.tonnel.network"  # Заменит :authority
            request.headers["accept"] = "*/*"
            request.headers["accept-encoding"] = "gzip, deflate, br, zstd"
            request.headers["accept-language"] = "en-GB,en-US;q=0.9,en;q=0.8"
            request.headers["content-type"] = "application/json"
            request.headers["origin"] = "https://tonnel-gift.vercel.app"
            request.headers["priority"] = "u=1, i"
            request.headers["referer"] = "https://tonnel-gift.vercel.app/"
            request.headers["sec-ch-ua"] = (
                '"Not(A:Brand";v="99", "Google Chrome";v="133", "Chromium";v="133"'
            )
            request.headers["sec-ch-ua-mobile"] = "?0"
            request.headers["sec-ch-ua-platform"] = '"macOS"'
            request.headers["sec-fetch-dest"] = "empty"
            request.headers["sec-fetch-mode"] = "cors"
            request.headers["sec-fetch-site"] = "cross-site"
            request.headers["user-agent"] = (
                "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36"
            )

            # Меняем referrer-policy
            request.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"

    def open_page(self, url, check_element, by=By.CSS_SELECTOR):
        log.info(f"Try to open: {url}")
        self.driver.get(url)

        if not self._retry_until_loaded(by, check_element):
            self.close_browser()

            raise Exception("Page load error.")

    def refresh_page(self):
        self.driver.refresh()

    def close_browser(self):
        self.driver.quit()

    def _retry_until_loaded(self, by, value, max_retries=3):  # [TODO] Change method name
        """
        Reload until the page loads successfully.

        :param max_retries: Max retries if the page fails to load
        """
        for attempt in range(max_retries):
            log.info(f"Checking page load: attempt ({attempt + 1}/{max_retries})")

            if self._is_element_present(by, value):
                return True

            self.driver.refresh()

        log.error(f"Page failed to load after retries")

        return False

    def _is_element_present(self, by, value, timeout=10):
        """Checks whether the item has been loaded in the specified time."""
        try:
            WebDriverWait(self.driver, timeout).until(
                EC.presence_of_element_located((by, value))
            )
            log.info('Page was load')
            return True

        except TimeoutException:
            log.warning(f"Element not found: {value} (Waited {timeout}s)")
            return False
