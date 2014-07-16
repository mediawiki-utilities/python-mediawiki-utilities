import time
import logging

import requests

logger = logging.getLogger("mw.util.api.session")

from .functions import none_or


class Session:
    def __init__(self, uri, headers=None, failure_threshold=None, wait_step=2):
        if uri is None:
            raise TypeError("uri must not be None")

        self.uri = str(uri)
        self.headers = headers if headers is not None else {}
        self.session = requests.Session()

        self.failure_threshold = none_or(failure_threshold, int)
        self.wait_step = float(wait_step)

        self.failed = 0

    def __sleep(self):
        time.sleep(self.failed * (self.wait_step ** self.failed))

    def get(self, params, **kwargs):
        return self.request('GET', params, **kwargs)

    def post(self, params, **kwargs):
        return self.request('POST', params, **kwargs)

    def request(self, type, params):
        try:
            result = self.session.request(type, self.uri, params=params)
            self.failed = 0
            return result
        except (requests.HTTPError, requests.ConnectionError, requests.Timeout):
            self.failed += 1

            if self.failed > self.failure_threshold:
                self.failed = 0
                raise
            else:
                self.__sleep()
                self.request(type, params)
