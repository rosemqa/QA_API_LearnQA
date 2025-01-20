from services.user.user_api import UserAPI


class BaseTest:
    def setup_method(self):
        self.api_user = UserAPI()
