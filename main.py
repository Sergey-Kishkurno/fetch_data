import os
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

    config = Config("./config.yml").get_config()

    ld = Loader (
        config['url'],
        _creds,
        config['headers'],
        config['dates']['start_date'],
        config['dates']['end_date']
    )

    try:
        ld.load()
    except Exception as e:
        pprint(e)


if __name__ == '__main__':
    app()
