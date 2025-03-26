import requests


class RestAdapter:
    def __init__(self, base_url: str, headers: dict = None) -> None:
        self._base_url = base_url
        self._headers = headers if headers else {}

    def _request(self, method: str, endpoint: str, **kwargs) -> dict:
        url = f"{self._base_url}{endpoint}"

        response = requests.request(method, url, headers=self._headers, **kwargs)
        json = response.json()

        if not (199 < response.status_code < 300) or json["success"] == False:
            raise Exception(f"Status Code: {response.status_code} {json["message"]}")

        return json

    def get(self, endpoint: str, **kwargs) -> dict:
        return self._request("GET", endpoint, **kwargs)

    def post(self, endpoint: str, **kwargs) -> dict:
        return self._request("POST", endpoint, **kwargs)
