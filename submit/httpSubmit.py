# -*- coding: utf-8 -*-

import requests

import util
from submit.submit import Submit
from util import checkKey


class HttpSubmit(Submit):
    HEADERS = {
        'Accept': "application/json;q=0.9;charset=utf-8",
        'User-Agent': "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36 Perfmon/1.0 (Client 1.0) Trust-Agent/1.0"
    }

    def __init__(self, config: dict, retry: int = 3, capacity: int = 20, timeout: int = 10000):
        super().__init__(capacity, timeout)
        self.retry = retry
        self.session = requests.Session()
        self.config = config
        self.name = checkKey("agent_name", self.config, str, "config")
        self.url = checkKey("server", self.config, str, "config")
        util.checkUrl(self.url)

    def checkResponse(self, response: requests.Response):
        assert response.status_code == 200, f"Submit server response status code '{response.status_code}'."
        json_t = response.json()
        assert "errno" in json_t, "Submit server response json has no errno key"
        if json_t['errno'] != 0:
            raise RuntimeError("Submit server response error({ERRNO}){ERROR}".format(
                ERRNO=json_t['errno'], ERROR=f": {json_t['error']}" if "error" in json_t else ""))
        return json_t

    def send(self) -> bool:
        if len(self.buf) <= 0:
            return False
        errmsg = []
        result = ""
        for i in range(self.retry):
            try:
                res = self.session.post(self.url, json=self.buf, headers=HttpSubmit.HEADERS)
                self.checkResponse(res)
                result = res.content
                break
            except BaseException as e:
                errmsg.append(str(e))
        if result:
            self.logger.debug("HttpSubmit: data has been sent.")
            return True
        else:
            self.logger.debug("HttpSubmit: data send failure.")
            for index, content in enumerate(errmsg):
                self.logger.debug(f"==> (try {index + 1}): {content}")
            return False
