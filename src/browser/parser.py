import json

import yaml
from seleniumwire import webdriver
from seleniumwire.utils import decode

from src.constants import API_LIST_GIFTS_URL


class PageParser:

    def __init__(self, driver: webdriver.Chrome):
        self.driver: webdriver.Chrome = driver

    def get_fetch_requests(self, endpoint):
        for req in reversed(self.driver.requests):
            res = req.response
            if res and req.url == endpoint:
                body = decode(res.body, res.headers.get("Content-Encoding", "identity"))
                return body


class TonnelRelayerParser(PageParser):
    def __init__(self, driver, config_path):
        super().__init__(driver)
        self.config = self.load_config(config_path)


    def load_config(self, path):
        with open(path, "r", encoding="utf-8") as file:
            return yaml.safe_load(file)

    def get_gifts(self):
        data = self.get_fetch_requests(API_LIST_GIFTS_URL)
        if data:
            return json.loads(data)

    def check_by_name_and_price(self):

        nfts = self.get_gifts()

        filters = self.config['filters'][0]['price']

        filtered_nfts = []

        if nfts:
            for nft in nfts:
                for filter in filters:
                    if nft['name'] == filter['collection_name'] and nft['price'] <= filter['buy_price']:
                        filtered_nfts.append(nft)
        print('FILTERED_NFTS\n')
        for n in filtered_nfts:
            print(f' - {n['name']} - {n['model']}: {n['price']} TON')
        print('\n\n\n\n\n\n')

        return filtered_nfts

