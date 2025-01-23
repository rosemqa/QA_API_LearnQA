import allure
import pytest
from config.base_test import BaseTest
from config.data import AuthDataDefaultUser
from services.user.payloads import Payloads, long_field_value, excluded_fields


class TestUser(BaseTest):
    # @pytest.fixture()
    # def login_default_user(self):
    #     self.email = AuthDataDefaultUser.EMAIL
    #     self.password = AuthDataDefaultUser.PASSWORD
    #
    #     login = self.api_user.login_user(self.email, self.password)
    #
    #     self.auth_cookie = login['auth_cookie']
    #     self.token = login['token']
    #     self.user_id = login['user_id']
    #
    # @pytest.fixture()
    # def create_new_user(self):
    #     self.new_user_id, register_data = self.api_user.create_user()
    #     self.new_user_email = register_data['email']
    #     self.new_user_password = register_data['password']
    #     self.new_user_username = register_data['username']
    #     self.new_user_firstname = register_data['firstName']
    #     self.new_user_lastname = register_data['lastName']
    #
    # @pytest.fixture()
    # def login_new_user(self, create_new_user):
    #     login = self.api_user.login_user(self.new_user_email, self.new_user_password)
    #     self.new_user_auth_cookie = login['auth_cookie']
    #     self.new_user_token = login['token']

    @allure.description('Can create (register) a new user')
    def test_create_user(self):
        self.api_user.create_user()

    @allure.description('Can not create user with already registered email')
    def test_create_user_with_existing_email(self):
        email = AuthDataDefaultUser.EMAIL
        user = self.api_user.create_user_with_specific_data(email=email)
        assert user == f"Users with email '{email}' already exists"

    @allure.description('Unable to create user with incorrect email format')
    @pytest.mark.parametrize('email', ['testmail.com', 'test @mail.com', 'test@mail.', 'test@mailcom', '@@mail.com'])
    @allure.tag('negative')
    def test_create_user_with_incorrect_email_format(self, email):
        response_text = self.api_user.create_user_with_specific_data(email=email)
        assert response_text == 'Invalid email format', f'Unexpected response content - {response_text}'

    @allure.description('Unable to create user with user name that is one symbol long')
    @allure.tag('negative')
    def test_create_user_with_too_short_name(self):
        username = 'A'
        response_text = self.api_user.create_user_with_specific_data(username=username)
        assert response_text == "The value of 'username' field is too short", \
            f'Unexpected response content - {response_text}'

    @allure.description('Unable to create user with user name that is more then 250 symbols long')
    @allure.tag('negative')
    def test_create_user_with_too_long_name(self):
        username = long_field_value()
        response_text = self.api_user.create_user_with_specific_data(username=username)
        assert response_text == "The value of 'username' field is too long", \
            f'Unexpected response content - {response_text}'

    @allure.description('Unable to create user if any of required fields are empty')
    @pytest.mark.parametrize('empty_field', excluded_fields)
    @allure.tag('negative')
    def test_create_user_with_empty_required_field(self, empty_field):
        response_text = self.api_user.create_user_with_specific_data(empty_field=empty_field)
        assert response_text == f"The value of '{empty_field}' field is too short", \
            f'Unexpected response content - {response_text}'

    @allure.description('Unable to create user if any of the required fields are missing')
    @pytest.mark.parametrize('missing_field', excluded_fields)
    @allure.tag('negative')
    def test_create_user_with_missing_required_field(self, missing_field):
        response_text = self.api_user.create_user_with_specific_data(missing_field=missing_field)
        assert response_text == f'The following required params are missed: {missing_field}', \
            f'Unexpected response content - {response_text}'

    @allure.description('Can edit all data of the newly created user')
    def test_edit_just_created_user(self, login_new_user, delete_new_user, check):
        new_user_data = login_new_user
        user_id = new_user_data['user_id']
        auth_cookie = new_user_data['auth_cookie']
        token = new_user_data['token']

        # EDIT USER
        new_data = Payloads().update_user
        edit = self.api_user.edit_auth_user_by_id(user_id, auth_cookie, token)
        assert edit.success == "!", 'Check the Success value from Edit method'

        # GET USER
        get = self.api_user.get_auth_user_by_id(user_id, auth_cookie, token)
        with check:
            assert get.email == new_data['email'], 'Email has not been changed'
        with check:
            assert get.firstName == new_data['firstName'], 'First name has not been changed'
        with check:
            assert get.lastName == new_data['lastName'], 'Last name has not been changed'
        with check:
            assert get.username == new_data['username'], 'Username name has not been changed'

    @allure.description('Unauthorized user can not edit a user info by ID')
    @allure.tag('negative')
    def test_edit_user_as_not_authed(self, login_new_user, delete_new_user):
        new_user_data = login_new_user
        edit = self.api_user.edit_user_by_id(new_user_data['user_id'])
        assert edit.error == 'Auth token not supplied', 'Check the error value'

    @allure.description('Authorized user can not edit another user')
    @allure.tag('negative')
    def test_edit_another_user(self, login_new_user, delete_new_user):
        new_user_data = login_new_user
        other_user_id = self.api_user.create_user()[0]
        auth_cookie = new_user_data['auth_cookie']
        token = new_user_data['token']

        edit = self.api_user.edit_user_by_id(other_user_id, auth_cookie, token)
        assert edit.error == 'This user can only edit their own data.', 'Check the error value'

    @allure.description('Field values cannot be changed to value that is one symbol long')
    @pytest.mark.parametrize('field', ['username', 'firstName', 'lastName'])
    @allure.tag('negative')
    def test_edit_user_with_too_short_name(self, login_new_user, delete_new_user, field):
        new_user_data = login_new_user
        edit = self.api_user.edit_user_with_specific_data(
            new_user_data['user_id'],
            new_user_data['auth_cookie'],
            new_user_data['token'],
            field=field,
            value='u'
        )
        assert edit.error == f"The value for field `{field}` is too short", f'Check error value for {field} field'

    @allure.description('Can login with email and password')
    def test_login_user(self, create_new_user):
        new_user_data = create_new_user
        login = self.api_user.login_user(new_user_data['email'], new_user_data['password'])
        assert login['user_id'] == int(new_user_data['user_id']), 'Check user ID value for Login method'

    @allure.description('Authorized user can get his user info by ID')
    def test_get_user_as_authed(self, check, login_new_user, delete_new_user):
        new_user_data = login_new_user
        user_id = new_user_data['user_id']
        user = self.api_user.get_auth_user_by_id(user_id, new_user_data['auth_cookie'], new_user_data['token'])
        with check:
            assert user.id == user_id, 'Check the user ID in response'
        with check:
            assert user.username == new_user_data['username'], 'Check the username ID in response'
        with check:
            assert user.firstName == new_user_data['firstname'], 'Check the first name in response'
        with check:
            assert user.lastName == new_user_data['lastname'], 'Check the last name in response'
        with check:
            assert user.email == new_user_data['email'], 'Check email in response'

    @allure.description('Authorized user can not get another user info by ID except for the user name')
    def test_get_another_user(self, login_new_user, delete_new_user):
        new_user_data = login_new_user
        another_user_id = AuthDataDefaultUser.USER_ID
        user = self.api_user.get_user_by_id(another_user_id, new_user_data['auth_cookie'], new_user_data['token'])
        assert user.username == AuthDataDefaultUser.USERNAME, 'Check username value'

    @allure.description('Unauthorized user can not get a user info by ID except for the user name')
    def test_get_user_as_not_authed(self):
        user_id = AuthDataDefaultUser.USER_ID
        user = self.api_user.get_user_by_id(user_id)
        assert user.username == AuthDataDefaultUser.USERNAME, 'Check username value'

    @allure.description('Can delete the just created user')
    def test_delete_user(self, login_new_user, delete_new_user):
        new_user_data = login_new_user
        user_id = login_new_user['user_id']

        # DELETE USER
        delete = self.api_user.delete_user_by_id(user_id, new_user_data['auth_cookie'], new_user_data['token'])
        assert delete.success == "!", 'Check the Success value from Delete method'

        # GET USER
        get = self.api_user.get_not_existed_user(user_id)
        assert get == 'User not found', 'Unexpected response text from Get method'

    @allure.description('Authorized user can not delete another user')
    def test_delete_another_user(self, login_new_user, delete_new_user):
        new_user_data = login_new_user
        other_user_id = self.api_user.create_user()[0]
        auth_cookie = new_user_data['auth_cookie']
        token = new_user_data['token']

        delete = self.api_user.delete_user_that_cannot_be_deleted(other_user_id, auth_cookie, token)
        assert delete.error == 'This user can only delete their own account.', 'Check the error value'

    @allure.description('Unable to delete a user whose data is protected from deletion')
    def test_delete_user_that_cannot_be_deleted(self, login_default_user):
        default_user_data = login_default_user
        delete = self.api_user.delete_user_that_cannot_be_deleted(
            default_user_data['user_id'],
            default_user_data['auth_cookie'],
            default_user_data['token']
        )
        assert delete.error == 'Please, do not delete test users with ID 1, 2, 3, 4 or 5.', 'Check the error value'

    @allure.description('User can be authorized after login')
    def test_is_user_authed(self, login_default_user):
        default_user_data = login_default_user
        user_id = self.api_user.get_user_id(default_user_data['auth_cookie'], default_user_data['token'])
        assert user_id == default_user_data['user_id'], \
            'User ID from Authed method is not equal to user ID from Login method'

    @allure.description('User can not be authorized w/o sending auth cookie or token')
    @pytest.mark.parametrize('condition', ['no cookie', 'no token'])
    @allure.tag('negative')
    def test_is_user_not_authed(self, login_default_user, condition):
        default_user_data = login_default_user
        if condition == 'no cookie':
            user_id = self.api_user.get_user_id(token=default_user_data['token'])
        else:
            user_id = self.api_user.get_user_id(auth_cookie=default_user_data['auth_cookie'])

        assert user_id == 0, f'User is authorized with condition "{condition}"'

    @allure.description('Cannot login with empty required fields')
    @pytest.mark.parametrize('empty_field', ['email', 'password', 'all fields'])
    @allure.tag('negative')
    def test_login_with_empty_fields(self, login_default_user, empty_field):
        default_user_data = login_default_user
        if empty_field == 'email':
            login = self.api_user.login_with_specific_data(password=default_user_data['password'])
        elif empty_field == 'password':
            login = self.api_user.login_with_specific_data(email=default_user_data['email'])
        else:
            login = self.api_user.login_with_specific_data()
        assert login == 'Invalid email/password supplied', f'Check error value for empty {empty_field}'

    @allure.description('Cannot login with wrong email or password')
    def test_login_with_wrong_credentials(self, login_default_user, check):
        default_user_data = login_default_user
        wrong_email = 'email@test.com'
        wrong_password = 'test123'
        wrong_password_login = self.api_user.login_with_specific_data(default_user_data['email'], wrong_password)
        wrong_email_login = self.api_user.login_with_specific_data(wrong_email, default_user_data['password'])
        with check:
            assert wrong_password_login == 'Invalid username/password supplied', f'Check error value for wrong password'
        with check:
            assert wrong_email_login == 'Invalid username/password supplied', f'Check error value for wrong email'
