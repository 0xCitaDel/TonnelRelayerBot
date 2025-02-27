import requests
import time
from requests.exceptions import RequestException

from src.config import config
from src.cypher import AESCipher


class HTTPClient:
    """Simple HTTP client for making requests with error handling."""

    def __init__(self, base_url=None, headers=None, timeout=10):
        """
        :param base_url: Optional base URL for all requests.
        :param headers: Default headers to use.
        :param timeout: Default request timeout.
        """
        self.base_url = base_url
        self.headers = headers or {}
        self.timeout = timeout

    def _prepare_url(self, endpoint):
        """Prepares the full URL by combining base_url and endpoint."""
        if self.base_url:
            return f"{self.base_url}/{endpoint}"
        return endpoint

    def get(self, endpoint, params=None):
        """Sends a GET request."""
        url = self._prepare_url(endpoint)
        try:
            response = requests.get(
                url, params=params, headers=self.headers, timeout=self.timeout
            )
            response.raise_for_status()
            return response.json()  # Try parsing JSON response
        except RequestException as e:
            print(f"HTTP GET Error: {e}")
            return None

    def post(self, endpoint, data=None, json=None):
        """Sends a POST request."""
        url = self._prepare_url(endpoint)
        try:
            response = requests.post(
                url, data=data, json=json, headers=self.headers, timeout=self.timeout
            )
            response.raise_for_status()
            return response.json()

        except RequestException as e:
            print(f"HTTP POST Error: {e}")
            return None


class TonnelRelayerHTTP(HTTPClient):

    def __init__(self, base_url=None, headers=None, timeout=10):
        super().__init__(base_url, headers, timeout)

        self.passphrase = "yowtfisthispieceofshitiiit"
        self.cipher = AESCipher(self.passphrase)

    def buy_gift(self, auth_data, gift_id, price):
        payload = self.get_buy_gift_payload(auth_data=auth_data, price=price)

        return self.post(endpoint=f"buyGift/{gift_id}", json=payload)


    def get_buy_gift_payload(self, auth_data: str, price):
        timestamp = self._get_unix_timestamp()
        # orig_price = self._get_original_price(price)

        return {
            "asset": "TON",
            "authData": auth_data,
            "price": price,
            "timestamp": timestamp,
            "wtf": self.cipher.encrypt(str(timestamp)),
        }

    def _get_unix_timestamp(self):
        return int(time.time())

    def _get_original_price(self, price):
        return price / 1.1


http_coffin = TonnelRelayerHTTP(
    base_url="https://gifts.coffin.meme/api",
    headers=config.get_headers["https://gifts2.tonnel.network"]
)
