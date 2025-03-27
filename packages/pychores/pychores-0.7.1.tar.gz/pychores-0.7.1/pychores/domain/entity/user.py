from dataclasses import dataclass


@dataclass
class User:
    email: str
    username: str
    id: int | None = None
