from faker import Faker

fake = Faker()


class Payloads:
    create_user = {
        'username': fake.user_name(),
        'firstName': fake.first_name_male(),
        'lastName': fake.last_name_male(),
        'email': fake.email(),
        'password': fake.password()
    }

    update_user = {
        'username': fake.user_name(),
        'firstName': fake.first_name_male(),
        'lastName': fake.last_name_male(),
        'email': fake.email(),
        'password': fake.password()
    }

    def update_users(self):
        return {
            'username': fake.user_name(),
            'firstName': fake.first_name_male(),
            'lastName': fake.last_name_male(),
            'email': fake.email(),
            'password': fake.password()
        }

    def create_users(self, email=None, user_name=None):
        if email is None:
            email = fake.email()
        if user_name is None:
            user_name = fake.user_name()
        return {
            'username': user_name,
            'firstName': fake.first_name_male(),
            'lastName': fake.last_name_male(),
            'email': email,
            'password': fake.password()
        }


def long_field_value():
    """returns a word over 250 symbols long"""
    return ''.join(fake.random_letters(251)).title()


excluded_fields = [
    'username',
    'firstName',
    'lastName',
    'email',
    'password'
]
