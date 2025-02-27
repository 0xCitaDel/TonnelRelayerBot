from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

# PATH-constants
DRIVER_PATH = BASE_DIR / "chromedriver"
LOCAL_STORAGE_JSON_PATH = BASE_DIR / "local_storage.json"
CONFIG_PATH = BASE_DIR / "filters.json"

# API-constants
API_BASE_URL = "https://gifts2.tonnel.network"
API_VERSION = "/api"

API_GIFTS_URL = "/pageGifts"
API_INFO_URL = "/balance/info"

API_LIST_GIFTS_URL = API_BASE_URL + API_VERSION + API_GIFTS_URL
API_BALANCE_INFO_URL = API_BASE_URL + API_VERSION + API_INFO_URL
