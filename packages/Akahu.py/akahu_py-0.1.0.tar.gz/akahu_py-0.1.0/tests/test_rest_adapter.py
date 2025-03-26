from unittest import TestCase, mock
from akahu.rest_adapter import RestAdapter

import requests


class TestRestAdapter(TestCase):
    def setUp(self):
        self.rest_adapter = RestAdapter("", {})
        self.response = requests.Response()

    def test__request_get_good_request(self):
        self.response.status_code = 200
        self.response._content = (
            '{"success": "true", "message": "placeholder"}'.encode()
        )

        with mock.patch("requests.request", return_value=self.response):
            result = self.rest_adapter._request("GET", "")
            self.assertDictEqual(result, {"success": "true", "message": "placeholder"})

    def test__request_get_bad_request(self):
        with mock.patch("requests.request", side_effect=requests.RequestException):
            with self.assertRaises(Exception):
                self.rest_adapter._request("GET", "")

    def test__request_get_404_request(self):
        self.response.status_code = 404

        with mock.patch("requests.request", return_value=self.response):
            with self.assertRaises(Exception):
                self.rest_adapter._request("GET", "")

    def test__request_serverside_failure(self):
        self.response.status_code = 200
        self.response._content = '{"success": false, "message": "placeholder"}'.encode()

        with mock.patch("requests.request", return_value=self.response):
            with self.assertRaises(Exception):
                self.rest_adapter._request("", "")
