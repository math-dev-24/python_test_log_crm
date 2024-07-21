from Models.userModel import UserModel, get_all_users
from faker import Faker


class UserController:
    __userModel = UserModel

    def generate_users(self, n: int = 10) -> None:
        """
        :param n: generate n users. Default is 10.
        :return: void
        """
        fake = Faker(locale="fr_FR")
        for _ in range(n):
            new_user = self.__userModel(
                fake.first_name(), fake.last_name(), fake.email(), fake.phone_number(), fake.address()
            )
            new_user.save(validate=True)

    @classmethod
    def get_all_users(cls):
        return get_all_users()


if __name__ == "__main__":
    user_controller = UserController()
    user_controller.generate_users(10)
    print(user_controller.get_all_users())


