import logging
import requests


class BaseRequest:
    def __init__(self, url: str, headers: dict = None):
        self.base_url = url
        self.headers = headers

    def _request(self, url: str, request_type: str, data: dict = None, expected_error=False) -> dict:
        stop_flag = False
        count = 0
        while not stop_flag and count < 5:
            match request_type:
                case 'GET':
                    response = requests.get(url, headers=self.headers)
                case 'POST':
                    response = requests.post(
                        url, data=data, headers=self.headers)
                case 'PUT':
                    response = requests.put(
                        url, data=data, headers=self.headers)
                case _:
                    response = requests.delete(url)

            status = response.status_code
            if expected_error or response.ok:
                stop_flag = True

            if status != 200:
                logging.warning(status)

            count += 1

        resp = {
            'method': request_type,
            'url': response.url,
            'status_code': status,
            'json': response.json(),
        }

        logging.info(resp)
        return resp

    def get(self, endpoint: str = "", endpoint_id: str = "", expected_error=False) -> dict:
        url = f'{self.base_url}/{endpoint}/{endpoint_id}'
        response = self._request(url, 'GET', expected_error=expected_error)
        return response

    def post(self, endpoint: str = "", endpoint_id: str = "", body: str = "") -> dict:
        url = f'{self.base_url}/{endpoint}/{endpoint_id}'
        response = self._request(url, 'POST', data=body)
        return response

    def put(self, endpoint: str = "", endpoint_id: str = "", body: str = "") -> dict:
        url = f'{self.base_url}/{endpoint}/{endpoint_id}'
        response = self._request(url, 'PUT', data=body)
        return response

    def delete(self, endpoint: str = "", endpoint_id: str = "") -> dict:
        url = f'{self.base_url}/{endpoint}/{endpoint_id}'
        response = self._request(url, 'DELETE')
        return response
