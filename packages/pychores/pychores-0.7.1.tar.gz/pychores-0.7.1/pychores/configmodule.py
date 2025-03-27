import os

DEFAULT_SECRET = "do not tell anyone this is a secret"


class Config:
    DEBUG = False
    TESTING = False
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.getenv("FLASK_SECRET") or DEFAULT_SECRET
    PG_HOST = os.getenv("POSTGRES_HOST") or "localhost"
    JWT_ACCESS_TOKEN_EXPIRES = False
    KEYCLOAK_SERVER_URL = os.getenv("KEYCLOAK_SERVER_URL")
    KEYCLOAK_REALM_NAME = os.getenv("KEYCLOAK_REALM_NAME")
    KEYCLOAK_CLIENT_ID = os.getenv("KEYCLOAK_CLIENT_ID")

    KEYCLOAK_ISSUER = f"{KEYCLOAK_SERVER_URL}/realms/{KEYCLOAK_REALM_NAME}"

    @staticmethod
    def get_config(env):
        if env == "development":
            return Development()
        if env == "production":
            return Production()
        if env == "test":
            return Test()
        return Production()


class Production(Config):
    def __init__(self):
        if self.SQLALCHEMY_DATABASE_URI is None:
            raise ValueError(
                "Database must be set in production mode, set DATABASE_URL env var"
            )
        if self.SECRET_KEY == DEFAULT_SECRET:
            raise ValueError(
                "Secret key can't be default in production, set FLASK_SECRET env var"
            )


class Development(Config):
    DEBUG = True
    ENV = True

    def __init__(self):
        if self.SQLALCHEMY_DATABASE_URI is None:
            self.SQLALCHEMY_DATABASE_URI = "sqlite:///chores.db"
        self.KEYCLOAK_SERVER_URL = "http://localhost:8080"
        self.KEYCLOAK_REALM_NAME = "chores-dev"
        self.KEYCLOAK_CLIENT_ID = "chores-dev-app"
        self.KEYCLOAK_ISSUER = (
            f"{self.KEYCLOAK_SERVER_URL}/realms/{self.KEYCLOAK_REALM_NAME}"
        )


class Test(Config):
    DEBUG = True
    ENV = True

    def __init__(self):
        self.SQLALCHEMY_DATABASE_URI = (
            f"postgresql://chores@{self.PG_HOST}/kinky_chores_tests"
        )
