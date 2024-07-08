import json
from flask import request, _request_ctx_stack
from functools import wraps
from jose import jwt
from urllib.request import urlopen

AUTH0_DOMAIN = 'dev-bziyhi8qwaekwd3z.us.auth0.com'
ALGORITHMS = ['RS256']
API_AUDIENCE = 'image'

# AuthError Exception
'''
AuthError Exception
A standardized way to communicate auth failure modes
'''


class AuthError(Exception):
    def __init__(self, error, status_code):
        self.error = error
        self.status_code = status_code


# Auth Header

'''
@TODO implement get_token_auth_header() method
    it should attempt to get the header from the request
        it should raise an AuthError if no header is present
    it should attempt to split bearer and the token
        it should raise an AuthError if the header is malformed
    return the token part of the header
'''


def get_token_auth_header():
    if 'Authorization' not in request.headers:
        raise AuthError({
            'code': 'Authorization is not in request',
            'description': 'Authorization is not in request'
        }, 401)
  
    auth_header = request.headers['Authorization']
    header_parts = auth_header.split(' ')

    if len(header_parts) != 2:
        raise AuthError({
            'code': 'invalid_header',
            'description': 'Token is invalid'
        }, 401)
    elif header_parts[0].lower() != 'bearer':
        raise AuthError({
            'code': 'invalid_header',
            'description': 'Header should start with bearer'
        }, 401)
    return header_parts[1]


'''
@TODO implement check_permissions(permission, payload) method
    @INPUTS
        permission: string permission (i.e. 'post:drink')
        payload: decoded jwt payload

'''


def check_permissions(permission, payload):
    if 'permissions' not in payload:
        raise AuthError({
            'code': 'invalid claims',
            'description': 'Permissions not found'
        }, 400)
    
    if permission not in payload['permissions']:
        raise AuthError({
            'code': 'unauthorized',
            'description': 'Permission is not allowed'
        }, 401)        
    
    return True

'''
@TODO implement verify_decode_jwt(token) method
    @INPUTS
        token: a json web token (string)

    it should be an Auth0 token with key id (kid)
    it should verify the token using Auth0 /.well-known/jwks.json
    it should decode the payload from the token
    it should validate the claims
    return the decoded payload
'''


def verify_decode_jwt(token):

    jsonUrl = urlopen(f'https://{AUTH0_DOMAIN}/.well-known/jwks.json')
    jwks = json.loads(jsonUrl.read())
    
    unverifiedHeader = jwt.get_unverified_header(token)
    
    rsaKey = {}
    if 'kid' not in unverifiedHeader:
        print('Authorization malformed')
        raise AuthError({
            'code': 'invalid_header',
            'description': 'Authorization malformed'
        }, 401)

    for key in jwks['keys']:
        if key['kid'] == unverifiedHeader['kid']:
            rsaKey = {
                'kty': key['kty'],
                'kid': key['kid'],
                'use': key['use'],
                'n': key['n'],
                'e': key['e'],
            }
    
    if rsaKey:
        try:
            payload = jwt.decode(
                token,
                rsaKey,
                algorithms=ALGORITHMS,
                audience=API_AUDIENCE,
                issuer='https://' + AUTH0_DOMAIN + '/'
            )

            return payload

        except jwt.ExpiredSignatureError as error:
            print(error)
            raise AuthError({
                'code': 'token_expired',
                'description': 'Token expired.'
            }, 401)

        except jwt.JWTClaimsError as error:
            print(error)
            raise AuthError({
                'code': 'invalid_claims',
                'description': 'Incorrect claims. Check the audience and issuer.'
            }, 401)
        except Exception as error:
            print(error)
            raise AuthError({
                'code': 'invalid_header',
                'description': 'Unable to parse auth token.'
            }, 400)
    raise AuthError({
                'code': 'invalid_header',
                'description': 'Unable to find the appropriate key.'
            }, 400)


'''
@TODO implement @requires_auth(permission) decorator method
    @INPUTS
        permission: string permission (i.e. 'post:drink')
'''
def requires_auth(permission=''):
    def requires_auth_decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
                jwt = get_token_auth_header()
                try:
                    payload = verify_decode_jwt(jwt)
                except Exception as error:
                    print(error)
                    raise AuthError({
                        'code': 'invalid token',
                        'description': 'Could not verify token'
                    }, 400)
                check_permissions(permission, payload)
                return f(payload, *args, **kwargs)
        return wrapper          
    return requires_auth_decorator
