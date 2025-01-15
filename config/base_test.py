from services.user.user_api import UserAPI


class BaseTest:
    @staticmethod
    def setup_method(self):
        self.api_user = UserAPI()
