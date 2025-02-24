import json


class ConfigLoader:
    def __init__(self, config_path="config.json"):
        with open(config_path, "r", encoding="utf-8") as file:
            self.config = json.load(file)

    @property
    def is_debug(self):
        return self.config['debug']

    @property
    def selenium_options(self):
        options = self.config["selenium"]
        return options

    @property
    def headless_mode(self):
        return self.selenium_options['headless']

    @property
    def use_proxy(self):
        return self.selenium_options['use_proxy']

    @property
    def get_proxy(self):
        return self.selenium_options['proxy']

    @property
    def get_headers(self):
        return self.config["headers"]


config = ConfigLoader()
