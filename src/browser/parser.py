import json
import time
from pprint import pprint as print
from typing import Dict, List, Optional

from seleniumwire import webdriver
from seleniumwire.utils import decode

from src.constants import API_LIST_GIFTS_URL, API_BALANCE_INFO_URL
from src.utils.new_elements_tracker import NewElementsTracker


class PageParser:

    def __init__(self, driver: webdriver.Chrome):
        self.driver: webdriver.Chrome = driver
        self.seen_requests = set()

    def get_fetch_requests(self, endpoint):
        while True:
            for req in reversed(self.driver.requests):
                res = req.response

                if res and req.url == endpoint and req.id not in self.seen_requests:
                    self.seen_requests.add(req.id)

                    body = decode(
                        res.body, res.headers.get("Content-Encoding", "identity")
                    )
                    data = json.loads(body)

                    if data[0]["status"] != "forsale":
                        break

                    return data

    def get_fetch_post_data(self, endpoint):
        for req in reversed(self.driver.requests):
            res = req.response

            if res and req.url == endpoint and req.method == "POST":
                self.seen_requests.add(req.id)
                req_body = req.body.decode('utf-8') if req.body else 'No Data'

                return json.loads(req_body)
        return {}


class TonnelRelayerParser(PageParser):

    def __init__(self, driver, filters_path, tracker: NewElementsTracker):
        super().__init__(driver)
        self.tracker = tracker
        self.filters = self._load_filters(filters_path)

    def get_last_gifts(self) -> Optional[List[Dict]]:
        return self.get_fetch_requests(API_LIST_GIFTS_URL)

    @property
    def get_balance_info(self):
        return self.get_fetch_post_data(API_BALANCE_INFO_URL)

    def filter_by_config(self):
        new_gifts = self.tracker.check_new_elements(self.get_last_gifts())

        filtered_nfts = []

        if new_gifts:
            for gift in new_gifts:
                for filter in self.filters:
                    if self.is_valid(gift, filter):
                        print(f"{gift['name']} - {gift['model']}: {gift['price']} TON")
                        filtered_nfts.append(gift)

        return filtered_nfts

    def is_valid(self, gift, filter):
        return (
            self.filter_by_name(gift, filter)
            and self.filter_by_model(gift, filter)
            and self.filter_by_price(gift, filter)
            and self.filter_by_currency(gift, filter)
            and self.filter_by_ids(gift, filter)
        )

    def filter_by_name(self, g: Dict, f: Dict) -> bool:
        """Filters by gift name"""
        return g["name"] == f["gift_name"]

    def filter_by_model(self, g: Dict, f: Dict) -> bool:
        """Filters by model (if specified)"""

        return f["model"] is None or g["model"] == f["model"]

    def filter_by_price(self, g: Dict, f: Dict):
        """Filters by price range"""
        min_price, max_price = f["price_range"]

        return min_price <= g["price"] <= max_price

    def filter_by_currency(self, g: Dict, f: Dict):
        """Filters by currency"""
        return g["asset"] == f["currency"]

    def filter_by_ids(self, g: Dict, f: Dict):

        return not f["gift_ids"] or g["gift_num"] in f["gift_ids"]

    def _load_filters(self, path):
        with open(path, "r", encoding="utf-8") as file:
            return json.load(file)
