import os
import yaml
from dotenv import load_dotenv
from pprintpp import pprint

from config import Config
from loader import Loader


def app():

    dotenv_path = os.path.join(os.path.dirname(''), '.env')
    if os.path.exists(dotenv_path):
        load_dotenv(dotenv_path)
    _creds = {
        "username": os.getenv('USERNAME'),
        "password": os.getenv('PASSWORD')
    }

    # TODO: url, endpoints - to be loaded via Config class
    config = Config("./config.yml").get_config()
    # pprint(f"TODO: Loaded from YAML file configuration: {config.get_config()}")
    # config.get_config()

    url = "https://robot-dreams-de-api.herokuapp.com"

    headers = {"content-type": "application/json"}
    start_date = "2021-04-01"
    end_date = "2021-04-01"

    ld = Loader (
        config['url'],
        _creds,
        config['headers'],
        config['dates']['start_date'],
        config['dates']['end_date']
    )
    # ld = Loader(url, _creds, headers, start_date, end_date)
    try:
        ld.load()
    except Exception as e:
        pprint(e)


if __name__ == '__main__':
    app()
