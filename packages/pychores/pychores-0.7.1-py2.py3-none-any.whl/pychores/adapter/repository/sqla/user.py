from pychores.domain.entity.user import User
from pychores.domain.use_cases.verify_user import IVerifyUserRepository, UserNotFound
from pychores.model import DeferedSession
from pychores.model import User as DbUser


class UserRepo(IVerifyUserRepository):
    def __init__(self):
        self.session = DeferedSession.get_session_local()

    def save_user(self, user: User):
        db_user = DbUser(username=user.username, email=user.email)

        self.session.add(db_user)
        self.session.commit()

    def fetch_by_email(self, email: str) -> User:
        user = self.session.query(DbUser).filter_by(email=email).first()
        if user is None:
            print(f"user with email {email} not found")
            raise UserNotFound
        return user
