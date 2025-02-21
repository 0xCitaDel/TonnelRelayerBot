# 1. Add to Browser Chrome
# https://chromewebstore.google.com/detail/manage-localstorage/hjbkmghihndbbjggaiocmlihachebmcn
# 2. Press "Export" -> "Copy" -> Paste into local_storage.json file"

from src.bot.bot_launcher import BotLauncher

if __name__ == "__main__":
    with BotLauncher() as bot:
        bot.run()
