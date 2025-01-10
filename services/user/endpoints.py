from config.config import BASE_URL


class Endpoints:
    login = f'{BASE_URL}/user/login'
    create_user = f'{BASE_URL}/user'
    get_user_id = f'{BASE_URL}/user/auth'
    get_user_info_by_id = lambda self, user_id: f'{BASE_URL}/user/{user_id}'
    update_user_by_id = lambda self, user_id: f'{BASE_URL}/user/{user_id}'
    delete_user_by_id = lambda self, user_id: f'{BASE_URL}/user/{user_id}'
