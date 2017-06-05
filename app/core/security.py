import json
import urllib

from auth0.v3.authentication import GetToken
from flask_login import UserMixin
from jose import jwt
from sqlalchemy import Column, String, Enum, Boolean

from app.errors import AppError, JWTExpiredError

_authenticated = dict()


SECURITY_LEVELS = ['guest', 'user', 'manager', 'admin', 'all', 'developer']

class SqlalchemyUserMixin(UserMixin):
    id = Column(String(64), primary_key=True, nullable=False)
    level = Column(Enum(*SECURITY_LEVELS, name='user_levels'), nullable=False, default='admin')
    is_active = Column(Boolean, nullable=False, default=True)

    def get_id(self):
        return _authenticated.get(self.id, None)


class SecurityService(object):
    def __init__(self, user_s, domain=None, client_id=None, client_secret=None, callback_url=None):
        self._jwks = None
        self.user_s = user_s

        self.domain = domain
        self.client_id = client_id
        self.client_secret = client_secret
        self.callback_url = callback_url

    def is_level_sufficient(self, user, level):
        return SECURITY_LEVELS.index(user.level) >= SECURITY_LEVELS.index(level)

    def get_jwks(self):
        if self._jwks is None:
            try:
                jsonurl = urllib.urlopen('https://' + self.domain + '/.well-known/jwks.json')
                self._jwks = json.loads(jsonurl.read())
            except IOError:
                raise AppError('could not load /.well-known/jwks.json from auth0')
        return self._jwks

    def fetch_jwt(self, code):
        get_token = GetToken(self.domain)
        return get_token.authorization_code(
            client_id=self.client_id,
            client_secret=self.client_secret,
            code=code,
            redirect_uri=self.callback_url)['id_token']

    def authenticate(self, token, clean=False):
        decoded_token = self._authenticate_jwt(token, clean)

        user_id = decoded_token['sub']
        user = self.user_s.get(user_id)
        if not user:
            user_model = self.user_s.__model__
            user = self.user_s.save(user_model(
                id=user_id,
                name=decoded_token['name']))

        return user

    def _authenticate_jwt(self, token, clean):
        if token in _authenticated and not clean:
            return self._auth_jwt_exp(token)

        token_decoded = self._auth_jwt_all(token)
        if token_decoded is not None:
            _authenticated[token_decoded['sub']] = token

        return token_decoded

    def _auth_jwt_exp(self, token):
        return self._auth_jwt_all(token, {
            'verify_signature': False,
            'verify_aud': False,
            'verify_iat': False,
            'verify_nbf': False,
            'verify_iss': False,
            'verify_sub': False,
            'verify_jti': False,
        })

    def _auth_jwt_all(self, token, options=None):
        jwks = self.get_jwks()
        unverified_header = jwt.get_unverified_header(token)
        rsa_key = {}
        for key in jwks['keys']:
            if key['kid'] == unverified_header['kid']:
                rsa_key = {
                    'kty': key['kty'],
                    'kid': key['kid'],
                    'use': key['use'],
                    'n': key['n'],
                    'e': key['e']
                }
        if rsa_key:
            try:
                return jwt.decode(
                    token=token,
                    key=rsa_key,
                    algorithms=unverified_header['alg'],
                    options=options,
                    audience=self.client_id)
            except jwt.ExpiredSignatureError:
                raise JWTExpiredError()
            except jwt.JWTClaimsError:
                raise AppError('JWTClaimsError')
            except Exception:
                raise AppError('Unable to parse authentication token')
        raise AppError('Unable to find appropriate key')
