from abc import ABC, abstractmethod

from pychores.domain.entity.chore import Chore


class IGetChores(ABC):
    @abstractmethod
    def get_chores(self, username: str) -> list[Chore]:
        """return a list of Chore for username"""


class GetUserChores:
    def __init__(self, repo: IGetChores):
        self.repo = repo

    def execute(self, username: str) -> list[Chore]:
        chores = self.repo.get_chores(username)
        overdues = sorted(
            filter(lambda x: x.is_overdue, chores),
            key=lambda x: x.priority_rate,
            reverse=True,
        )
        planed = sorted(
            filter(lambda x: not x.is_overdue, chores), key=lambda x: x.next_execution
        )
        return overdues + planed
