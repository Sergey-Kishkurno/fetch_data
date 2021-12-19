import os
import requests
import json
from pprintpp import pprint
from config import Config
from urllib.parse import urljoin

# url: https://robot-dreams-de-api.herokuapp.com

# endpoint: /auth
# payload: {"username": "rd_dreams", "password": "djT6LasE"}
# output type: JWT TOKEN

# endpoint: /out_of_stock
# payload: {"date": "2021-01-02"}
# auth: JWT <jwt_token>


class Loader:
    def __init__(self, url, creds, headers, date):
        self._file_basepath = "/files/"
        self._url = url
        self._creds = creds
        self._headers = headers
        self._date = date

    def _auth_for_load(self):
        url_auth = urljoin(self._url, "/auth")
        # pprint(url_auth)
        response = requests.post(url_auth, headers=self._headers, data=json.dumps(self._creds))
        # pprint(response)
        return response.json().get("access_token")

    def load(self) -> None:

        # pprint("--- Start loading... ---------------------")

        jwt = self._auth_for_load()

        # pprint(jwt)

        url_load = urljoin(self._url, "/out_of_stock")
        _headers = {'authorization': 'JWT {}'.format(jwt)}
        _data = {"date" : self._date}

        # pprint("_headers: ")
        # pprint(_headers)

        response = requests.get(url_load, headers=_headers, data=_data)
        data = response.json()

        # pprint(data)

        name = self._date
        self._save_to_file(data, name)

    def _save_to_file(self, data, name):

        _qname = self._file_basepath + name + ".txt"
        pprint(f"Full path to file: {_qname}")
        # os.chmod(_qname, 777)
        with open(_qname, 'w', encoding='utf-8') as f:
            f.write(json.dump(data))


def app():

    config = Config("./config.yml")
    pprint(f"Loaded from YAML file configuration:", config.get_config())

    # TODO: To be loaded via Config class
    url = "https://robot-dreams-de-api.herokuapp.com"
    creds = {
        "username": "rd_dreams",
        "password": "djT6LasE"
    }
    headers = {"content-type": "application/json"}
    date = "2021-12-15"

    ld = Loader(url, creds, headers, date)
    try:
        ld.load()
    except Exception as e:
        pprint(e)


if __name__ == '__main__':
    app()



