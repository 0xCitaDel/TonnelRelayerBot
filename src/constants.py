from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

# PATH-constants
DRIVER_PATH = BASE_DIR / "chromedriver"
LOCAL_STORAGE_JSON_PATH = BASE_DIR / "local_storage.json"
CONFIG_PATH = BASE_DIR / "config.yaml"

# API-constants
API_BASE_URL = "https://api.tonnel.network/gift/api"
API_GIFTS_URL = "/pageGifts"
API_LIST_GIFTS = API_BASE_URL + API_GIFTS_URL
