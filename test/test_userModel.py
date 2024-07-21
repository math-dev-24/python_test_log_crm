# ____ Imports _____
from Models.userModel import UserModel
from tinydb import TinyDB, table
from tinydb.storages import MemoryStorage
import pytest

USER = {
    "first_name": "Alex", "last_name": "Lemaire", "email": "alexlemaire@example.com",
    "phone_number": "0612345678", "address": "12 rue de la Gare"
}


@pytest.fixture
def setup_db():
    UserModel.DB = TinyDB(storage=MemoryStorage)


@pytest.fixture
def user(setup_db):
    tmp_user = UserModel(**USER)
    tmp_user.save()
    return tmp_user


def test_full_name(user):
    assert user.full_name == "Alex Lemaire"


def test_exists(user):
    assert user.exists() is True


def test_not_exists(setup_db):
    tmp_user = UserModel(**USER)
    assert tmp_user.exists() is False


def test_db_instance(user):
    assert isinstance(user.db_instance(), table.Document)
    assert user.db_instance() == USER


def test_no_db_instance(setup_db):
    tmp_user = UserModel(**USER)
    assert tmp_user.db_instance() is None


def test_check_names(setup_db):
    user_good = UserModel(**USER)
    USER['phone_number'] = "+éa]&2345678"
    user_bad = UserModel(**USER)

    with pytest.raises(ValueError) as err:
        user_bad.check_phone_number()
    assert "Phone number +éa]&2345678 is not valid" in str(err.value)

    user_good.save(validate=True)
    assert user_good.exists() is True


def test_check_name_empty(setup_db):
    USER['first_name'] = ""
    user_bad = UserModel(**USER)

    with pytest.raises(ValueError) as err:
        user_bad.check_names()
    assert "First name or last name is empty" in str(err.value)


def test_check_name_digits(setup_db):
    USER['first_name'] = "123"
    user_bad = UserModel(**USER)

    with pytest.raises(ValueError) as err:
        user_bad.check_names()
    assert "First name or last name contains digits or punctuation" in str(err.value)
