import yaml


class Config:
    def __init__(self, path):
        with open(path, 'r') as config_file:
            self.__config = yaml.safe_load(config_file)

    def get_config(self):
        return self.__config

