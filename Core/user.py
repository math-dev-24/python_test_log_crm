# ____ Models _____
from Models.userModel import UserModel as User
# ____ Imports _____
from pathlib import Path
import logging
import faker

fake = faker.Faker()
BASE_DIR = Path(__file__).resolve().parent.parent
# Logging
logging.basicConfig(filename=BASE_DIR.joinpath('logs/user/debug.log'), level=logging.DEBUG)
logging.basicConfig(filename=BASE_DIR.joinpath('logs/user/info.log'), level=logging.INFO)
logging.basicConfig(filename=BASE_DIR.joinpath('logs/user/warning.log'), level=logging.WARNING)
logging.basicConfig(filename=BASE_DIR.joinpath('logs/user/error.log'), level=logging.ERROR)


def get_user() -> User:
    """
    Generates a user
    :return:
        User: user
    """
    logging.info("Generating user")
    user = User(fake.first_name(), fake.last_name(), fake.email(), fake.phone_number(), fake.address())
    return user


def get_users(quantity: int = 10) -> list[User]:
    """
    :param quantity: Number of users to generate
    :return:
        list[User]: users
    """
    logging.info("Generating list of users")
    return [get_user() for _ in range(quantity)]


if __name__ == '__main__':
    list_of_users = get_users()
    print(list_of_users)
