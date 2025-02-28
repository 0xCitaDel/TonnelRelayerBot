# 1. Add to Browser Chrome
# https://chromewebstore.google.com/detail/manage-localstorage/hjbkmghihndbbjggaiocmlihachebmcn
# 2.1 Rename local_storage.json.dist to local_storage.json
# 2.2 Log into your telegram account from Chrome with Extenseion in step one
# 2.3 Open the extension when telegram is open then press "Export" -> "Copy" -> Paste into local_storage.json file"

from src.bot.bot_launcher import BotLauncher
from src.config import config

if __name__ == "__main__":
    with BotLauncher(task_disable=config.is_debug) as bot:
        bot.run()
