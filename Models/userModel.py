# ____ Imports _____
import re
import string
from tinydb import TinyDB, where, table
from pathlib import Path


class UserModel:
    __BASE_DIR = Path(__file__).resolve().parent.parent
    DB = TinyDB(__BASE_DIR.joinpath('dbUsers.json'))

    def __init__(self, first_name: str, last_name: str, email: str = "", phone_number: str = "", address: str = ""):
        """
        :param first_name: user first name
        :param last_name:  user last name
        :param email: user email
        :param phone_number: user phone number
        :param address: user address
        """
        self.first_name: str = first_name
        self.last_name: str = last_name
        self.email: str = email
        self.phone_number: str = phone_number
        self.address: str = address

    def __str__(self) -> str:
        return f"{self.full_name} \n{self.email} \n{self.phone_number} \n{self.address}"

    def __repr__(self) -> str:
        return f"User({self.first_name}, {self.last_name}, {self.email}, {self.phone_number}, {self.address})"

    @property
    def full_name(self) -> str:
        return f"{self.first_name} {self.last_name}"

    def db_instance(self) -> table.Document:
        return UserModel.DB.get((where('first_name') == self.first_name) & (where('last_name') == self.last_name))

    def delete(self) -> list[int]:
        if self.exists():
            return UserModel.DB.remove(doc_ids=[self.db_instance().doc_id])
        return []

    def exists(self) -> bool:
        return self.db_instance() is not None

    def save(self, validate: bool = False) -> int:
        if validate:
            self.checks()
        if self.exists():
            return -1
        else:
            return self.DB.insert(self.__dict__)

    def checks(self) -> None:
        self.check_names()
        self.check_phone_number()

    def check_phone_number(self) -> None:
        phone_digit = re.sub(r"[+()\s]*", "", self.phone_number)
        if len(phone_digit) < 10 or not phone_digit.isdigit():
            raise ValueError(f"Phone number {self.phone_number} is not valid")

    def check_names(self) -> None:
        if not self.first_name or not self.last_name:
            raise ValueError(f"First name or last name is empty")
        for char in self.first_name + self.last_name:
            if char in string.punctuation or char in string.digits:
                raise ValueError(f"First name or last name contains digits or punctuation")


def get_all_users() -> list[UserModel]:
    """
    :return: list of all users
    """
    list_of_users = []
    for user in UserModel.DB.all():
        tmp_user = UserModel(**user)
        list_of_users.append(tmp_user)
    return list_of_users
