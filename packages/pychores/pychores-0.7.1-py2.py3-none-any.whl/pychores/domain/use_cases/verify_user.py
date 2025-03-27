from abc import ABC, abstractmethod
from typing import Mapping

from pychores.domain.entity.user import User


class IVerifyUserRepository(ABC):
    @abstractmethod
    def fetch_by_email(self, email: str) -> User:
        """return a User by user_id"""

    @abstractmethod
    def save_user(self, user: User):
        """Save the domain part of user"""


class UserNotFound(Exception):
    pass


class VerfiyUser:
    def __init__(self, user_repo: IVerifyUserRepository):
        self.user_repo = user_repo

    def execute(self, token: Mapping[str, str]) -> User:
        try:
            user = self.user_repo.fetch_by_email(token["email"])
        except UserNotFound:
            user = User(
                email=token["email"],
                username=token["preferred_username"],
            )
            self.user_repo.save_user(user)
        return user
