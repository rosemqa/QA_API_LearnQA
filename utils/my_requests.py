import requests
import allure
from utils.logger import Logger


class MyRequests:
    @staticmethod
    def get(url: str, params: dict = None, data: dict = None, headers: dict = None, cookies: dict = None):
        Logger.add_request(url, params, data, headers, cookies, 'GET')
        response = requests.get(url, params=params, headers=headers, cookies=cookies)
        with allure.step(f'GET request to URL "{response.request.url}"'):
            Logger.add_response(response)
            return response

    @staticmethod
    def post(url: str, data: dict = None, json: dict = None, headers: dict = None, cookies: dict = None):
        with allure.step(f'POST request to URL "{url}"'):
            Logger.add_request(url, data, json, headers, cookies, 'POST')
            response = requests.post(url, data=data, json=json, headers=headers, cookies=cookies)
            Logger.add_response(response)
            return response

    @staticmethod
    def put(url: str, data: dict = None, json: dict = None, headers: dict = None, cookies: dict = None):
        with allure.step(f'PUT request to URL "{url}"'):
            Logger.add_request(url, data, json, headers, cookies, 'PUT')
            response = requests.put(url, data=data, json=json, headers=headers, cookies=cookies)
            Logger.add_response(response)
            return response

    @staticmethod
    def delete(url: str, data: dict = None, json: dict = None, headers: dict = None, cookies: dict = None):
        with allure.step(f'DELETE request to URL "{url}"'):
            Logger.add_request(url, data, json, headers, cookies, 'DELETE')
            response = requests.delete(url, data=data, json=json, headers=headers, cookies=cookies)
            Logger.add_response(response)
            return response
