import uuid
from http import HTTPStatus
from unittest import TestCase

from wallet.core.user.user import FetchUserRequest, UserRequest
from wallet.core.user.user_interactor import UserInteractor
from wallet.core.utils import KeyGenerator
from wallet.infra.in_memory.user_in_memory import UserInMemoryRepository


class TestUser(TestCase):
    def generate_api_key(self):
        return str(uuid.uuid4().hex)

    def setUp(self) -> None:
        self.generator = KeyGenerator()
        self.user_interactor = UserInteractor(UserInMemoryRepository(), self.generator)


class TestCreateAndGetUser(TestUser):
    def test_create_and_get_user(self) -> None:
        response = self.user_interactor.create_user(UserRequest("user1"))
        user_info = response.user_info
        if user_info is not None:
            user = self.user_interactor.fetch_user(FetchUserRequest(user_info.api_key))
            if user is not None:
                self.assertEqual(
                    user.get_username(),
                    "user1",
                )

    def test_status_code_created(self) -> None:
        self.assertEqual(
            self.user_interactor.create_user(UserRequest("user1")).status_code,
            HTTPStatus.CREATED,
        )

    def test_duplicate_username(self) -> None:
        self.user_interactor.create_user(UserRequest("user1"))
        self.assertEqual(
            self.user_interactor.create_user(UserRequest("user1")).status_code,
            HTTPStatus.CONFLICT,
        )

    def test_contains_username(self) -> None:
        self.assertEqual(self.user_interactor.contains_username("user2"), False)
        self.user_interactor.create_user(UserRequest("user1"))
        self.assertEqual(self.user_interactor.contains_username("user1"), True)

    def test_get_user_by_id(self) -> None:
        self.user_interactor.create_user(UserRequest("user1"))
        user = self.user_interactor.fetch_user_by_id(1)
        if user is not None:
            self.assertEqual(user.get_username(), "user1")

    def test_api_key_does_not_exist(self) -> None:
        self.assertEqual(self.user_interactor.fetch_user(FetchUserRequest("")), None)

    def test_id_does_not_exist(self) -> None:
        self.assertEqual(self.user_interactor.fetch_user_by_id(3), None)
