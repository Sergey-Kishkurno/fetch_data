from pprintpp import pprint
from urllib.parse import urljoin
import requests
import json
from datetime import date, datetime, timedelta


class Loader:
    def __init__(self, url, creds, headers, start_date, end_date):
        self._file_basepath = "files/"
        self._url = url
        self._creds = creds
        self._headers = headers
        self._start_date = start_date   # in format "2021-01-01"
        self._end_date = end_date       # in format "2021-12-15"

    def _auth_for_load(self):
        url_auth = urljoin(self._url, "/auth")
        # pprint(url_auth)
        response = requests.post(url_auth, headers=self._headers, data=json.dumps(self._creds))
        # pprint(response)
        return response.json().get("access_token")

    def load(self) -> None:

        # Authorize on the data service via JWT
        jwt = self._auth_for_load()

        # Prepare the general part of parameters
        url_load = urljoin(self._url, "/out_of_stock")
        _headers = {
            "authorization": 'JWT {}'.format(jwt),
            "content-type": "application/json"
        }

        # Prepare daily iteration between start_date and end_date
        sy, sm, sd = self._start_date.split('-')
        ey, em, ed = self._end_date.split('-')

        # Time measurements:
        time_loading_started = datetime.now()
        pprint('---- Start loading...--------------------------------------------------------------------------')
        pprint(f'---- Start_date =[{self._start_date}], end_date = [{self._end_date}] '
               f'----------------------------------------')
        pprint(f'---- Timestamp:{time_loading_started} -----------------------------------------------------')

        # The main cycle of iteration - loading and saving on daily basis
        for day in self.date_span(
                        date(int(sy), int(sm), int(sd)),
                        date(int(ey), int(em), int(ed)),
                        timedelta(days=1)
                    ):
            _data = json.dumps(
                       {"date": str(day)}
                    )
            _filename = self._file_basepath + str(day) + ".txt"
            pprint(f"Date in iteration: [{_data}], write in file with the name: {_filename}")
            try:
                self.__load_and_save_daily_data(url_load, _headers, _data, _filename)
            except Exception as e:
                pprint(e)

        # Final time measurements:
        time_loading_ended = datetime.now()
        td = time_loading_ended - time_loading_started
        pprint('---- Loading ended ----------------------------------------------------------------------------')
        pprint(f'---- Timestamp:{time_loading_started} -----------------------------------------------------')
        pprint(f'---- Downloading time:{td} ----------------------------------------------------------')

    def __load_and_save_daily_data(self, url, headers, data, filename):
        response = requests.get(url, headers=headers, data=data)
        response.raise_for_status()
        result = response.json()
        with open(filename, 'w+', encoding='utf-8') as f:
            f.write(json.dumps(result))

    def date_span(self, start_date, end_date, delta):
        current_date = start_date
        while current_date < end_date:
            yield current_date
            current_date += delta
