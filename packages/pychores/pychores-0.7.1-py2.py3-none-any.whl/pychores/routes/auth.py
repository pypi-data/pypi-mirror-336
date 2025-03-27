import json
from urllib.request import urlopen

from authlib.integrations.flask_oauth2 import ResourceProtector
from authlib.jose.rfc7517.jwk import JsonWebKey
from authlib.oauth2.rfc6749.resource_protector import TokenValidator
from authlib.oauth2.rfc7523 import JWTBearerTokenValidator
from flask import session

from pychores.adapter.repository.sqla.user import UserRepo
from pychores.domain.use_cases.verify_user import VerfiyUser


class ClientCredsTokenValidator(JWTBearerTokenValidator):
    def __init__(self, issuer):
        jsonurl = urlopen(f"{issuer}/protocol/openid-connect/certs")
        public_key = JsonWebKey.import_key_set(json.loads(jsonurl.read()))
        super().__init__(public_key)
        self.claims_options = {
            "exp": {"essential": True},
            "iss": {"essential": True, "value": issuer},
        }

    def validate_token(self, token, scopes, request):
        super().validate_token(token, scopes, request)
        verify_user(token)


class DummyValidator(TokenValidator):
    def __init__(self):
        public_key = "dummy"
        super().__init__(public_key)

    def authenticate_token(self, token_string):
        """We suppose there are no encoding at all and tokenstring is pure json"""
        return json.loads(token_string)

    def validate_token(self, token, scopes, request):
        verify_user(token)


require_auth = ResourceProtector()


def verify_user(token: dict):
    uc = VerfiyUser(UserRepo())
    user = uc.execute(token)
    session["username"] = user.username


def serialize_user(user, access_token=None):
    return {
        "username": user.username,
        "email": user.email,
        "id": user.id,
        "access_token": access_token,
    }
