import requests


class RestClient:
    def __init__(self, tesseract_pro):
        self.api_version = 'v1'
        self._tpro = tesseract_pro

    def get(self, endpoint, params=None):
        url = f"{self._tpro.server_url}/{self.api_version}/api/{endpoint}"
        headers = {"x-tesseractpro-api-key": self._tpro.api_token}

        response = requests.get(url, headers=headers, params=params)

        return response.json()

    def delete(self, endpoint, params=None):
        url = f"{self._tpro.server_url}/{self.api_version}/api/{endpoint}"
        headers = {"x-tesseractpro-api-key": self._tpro.api_token}

        response = requests.delete(url, headers=headers, params=params)

        print(response.json())

        return response.json()

    def put(self, endpoint, data=None):
        url = f"{self._tpro.server_url}/{self.api_version}/api/{endpoint}"
        headers = {"x-tesseractpro-api-key": self._tpro.api_token}
        response = requests.put(url, headers=headers, json=data)

        data = response.json()

        if isinstance(data, dict):
            if 'statuscode' in data and data['statusCode'] == 400:
                raise Exception(data['message'])

        return data

    def post(self, endpoint, data=None):
        url = f"{self._tpro.server_url}/{self.api_version}/api/{endpoint}"
        headers = {"x-tesseractpro-api-key": self._tpro.api_token}
        response = requests.post(url, headers=headers, json=data)

        data = response.json()

        if isinstance(data, dict):
            if 'statuscode' in data and data['statusCode'] == 400:
                raise Exception(data['message'])

        return data
