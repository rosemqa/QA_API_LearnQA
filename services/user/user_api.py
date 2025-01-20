import allure
from models.user_model import GetAuthUserModel, UserLoginModel, GetUserModel, LoginHeadersModel, LoginCookiesModel, \
    CreateUserModel, AuthedModel, SuccessModel, ErrorModel
from services.user.endpoints import Endpoints
from services.user.payloads import Payloads
from utils.helper import Helper
from utils.my_requests import MyRequests


class UserAPI(Helper):
    def __init__(self):
        self.endpoints = Endpoints()
        self.payloads = Payloads()

    @allure.step('Create a new user')
    def create_user(self):
        payload = self.payloads.create_users()
        response = MyRequests.post(
            url=self.endpoints.create_user,
            json=payload
        )
        assert response.status_code == 200, f'{response.status_code}, {response.content.decode("utf-8")}'
        self.attach_response(response.json())
        model = CreateUserModel(**response.json())
        user_id = model.id
        return user_id, payload

    @allure.step('Create a user with specific data')
    def create_user_with_specific_data(self, empty_field=None, missing_field=None, email=None, username=None):
        payload = self.payloads.create_users(email, username)
        payload[empty_field] = ''
        if missing_field:
            del payload[missing_field]
        response = MyRequests.post(
            url=self.endpoints.create_user,
            json=payload
        )
        assert response.status_code == 400, f'{response.status_code}, {response.content.decode("utf-8")}'
        self.attach_response(response.content.decode("utf-8"))
        return response.content.decode("utf-8")

    @allure.step('Edit user info by ID as authorized user')
    def edit_auth_user_by_id(self, user_id, auth_cookie, token):
        response = MyRequests.put(
            url=self.endpoints.update_user_by_id(user_id),
            cookies={'auth_sid': auth_cookie},
            headers={'x-csrf-token': token},
            json=self.payloads.update_user
        )
        assert response.status_code == 200, f'{response.status_code}, {response.content.decode("utf-8")}'
        self.attach_response(response.json())
        model = SuccessModel(**response.json())
        return model

    @allure.step('Edit user info by ID as unauthorized user')
    def edit_user_by_id(self, user_id, auth_cookie=None, token=None):
        response = MyRequests.put(
            url=self.endpoints.update_user_by_id(user_id),
            cookies={'auth_sid': auth_cookie},
            headers={'x-csrf-token': token},
            json=self.payloads.update_user
        )
        assert response.status_code == 400, f'{response.status_code}, {response.content.decode("utf-8")}'
        self.attach_response(response.json())
        model = ErrorModel(**response.json())
        return model

    @allure.step('Edit a user with specific data')
    def edit_user_with_specific_data(self, user_id, auth_cookie, token, field, value):
        payload = self.payloads.update_users()
        payload[field] = value
        response = MyRequests.put(
            url=self.endpoints.update_user_by_id(user_id),
            cookies={'auth_sid': auth_cookie},
            headers={'x-csrf-token': token},
            json=payload
        )
        assert response.status_code == 400, f'{response.status_code}, {response.content.decode("utf-8")}'
        self.attach_response(response.json())
        model = ErrorModel(**response.json())
        return model

    @allure.step('Get user id you are authorizes as OR get 0 if not authorized')
    def get_user_id(self, auth_cookie=None, token=None):
        response = MyRequests.get(
            url=self.endpoints.get_user_id,
            cookies={'auth_sid': auth_cookie},
            headers={'x-csrf-token': token}
        )
        assert response.status_code == 200, f'{response.status_code}, {response.content.decode("utf-8")}'
        self.attach_response(response.json())
        model = AuthedModel(**response.json())
        user_id = model.user_id
        return user_id

    @allure.step('Get user info by ID as unauthorized user')
    def get_user_by_id(self, user_id, auth_cookie=None, token=None):
        response = MyRequests.get(
            url=self.endpoints.get_user_info_by_id(user_id),
            cookies={'auth_sid': auth_cookie},
            headers={'x-csrf-token': token}
        )
        assert response.status_code == 200, f'{response.status_code}, {response.content.decode("utf-8")}'
        self.attach_response(response.json())
        model = GetUserModel(**response.json())
        return model

    @allure.step('Get user info by ID as authorized user')
    def get_auth_user_by_id(self, user_id, auth_cookie, token):
        response = MyRequests.get(
            url=self.endpoints.get_user_info_by_id(user_id),
            cookies={'auth_sid': auth_cookie},
            headers={'x-csrf-token': token}
        )
        assert response.status_code == 200, f'{response.status_code}, {response.content.decode("utf-8")}'
        self.attach_response(response.json())
        model = GetAuthUserModel(**response.json())
        return model

    @allure.step('Get not_existed/deleted user')
    def get_not_existed_user(self, user_id):
        response = MyRequests.get(
            url=self.endpoints.get_user_info_by_id(user_id)
        )
        assert response.status_code == 404, f'{response.status_code}, {response.content.decode("utf-8")}'
        self.attach_response(response.content.decode("utf-8"))
        return response.content.decode("utf-8")

    @allure.step('Delete a user by user ID')
    def delete_user_by_id(self, user_id, auth_cookie=None, token=None):
        response = MyRequests.delete(
            url=self.endpoints.delete_user_by_id(user_id),
            cookies={'auth_sid': auth_cookie},
            headers={'x-csrf-token': token}
        )
        assert response.status_code == 200, f'{response.status_code}, {response.content.decode("utf-8")}'
        self.attach_response(response.json())
        model = SuccessModel(**response.json())
        return model

    @allure.step('Delete a non-existent or protected user')
    def delete_user_that_cannot_be_deleted(self, user_id, auth_cookie, token):
        response = MyRequests.delete(
            url=self.endpoints.delete_user_by_id(user_id),
            cookies={'auth_sid': auth_cookie},
            headers={'x-csrf-token': token}
        )
        assert response.status_code == 400, f'{response.status_code}, {response.content.decode("utf-8")}'
        self.attach_response(response.json())
        model = ErrorModel(**response.json())
        return model

    @allure.step('Login user into the system')
    def login_user(self, email, password):
        response = MyRequests.post(
            url=self.endpoints.login,
            json={'email': email, 'password': password}
        )
        assert response.status_code == 200, f'{response.status_code}, {response.content.decode("utf-8")}'
        self.attach_response(response.json())
        model = UserLoginModel(**response.json())
        header_model = LoginHeadersModel(**response.headers)
        cookie_model = LoginCookiesModel(**response.cookies)
        auth_cookie = cookie_model.auth_sid
        token = header_model.token
        user_id = model.user_id
        return {'user_id': user_id, 'auth_cookie': auth_cookie, 'token': token}

    @allure.step('Login user with specific data')
    def login_with_specific_data(self, email=None, password=None):
        response = MyRequests.post(
            url=self.endpoints.login,
            json={'email': email, 'password': password}
        )
        assert response.status_code == 400, f'{response.status_code}, {response.content.decode("utf-8")}'
        self.attach_response(response.content.decode("utf-8"))
        return response.content.decode("utf-8")
