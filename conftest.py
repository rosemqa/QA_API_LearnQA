import pytest
from config.data import AuthDataDefaultUser
from services.user.user_api import UserAPI

api_user = UserAPI()


@pytest.fixture()
def login_default_user():
    email = AuthDataDefaultUser.EMAIL
    password = AuthDataDefaultUser.PASSWORD

    login = api_user.login_user(email, password)

    default_user_data = {
        'email': email,
        'password': password,
        'auth_cookie': login['auth_cookie'],
        'token': login['token'],
        'user_id': login['user_id']
    }
    return default_user_data


@pytest.fixture()
def create_new_user():
    new_user_id, register_data = api_user.create_user()
    new_user_info = {
        'user_id': new_user_id,
        'email': register_data['email'],
        'password': register_data['password'],
        'username': register_data['username'],
        'firstname': register_data['firstName'],
        'lastname': register_data['lastName']
    }
    return new_user_info


@pytest.fixture()
def login_new_user(create_new_user):
    new_user_info = create_new_user

    login = api_user.login_user(new_user_info['email'], new_user_info['password'])

    new_user_data = {
        'auth_cookie': login['auth_cookie'],
        'token': login['token']
    }
    new_user_data |= new_user_info
    return new_user_data


@pytest.fixture()
def delete_new_user(login_new_user):
    yield
    user_data = login_new_user
    api_user.delete_user_by_id(user_data['user_id'], user_data['auth_cookie'], user_data['token'])
