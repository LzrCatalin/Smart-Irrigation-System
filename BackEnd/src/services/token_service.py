import time
import jwt
from src.services.users_service import *

EKEY = 'f98d5d2f2f0142e2a8b2d9db07d5a92f302b'

def generate_token(p: dict, exp_time=3600) -> str:

    payload = {
        'iat': time.time(),
        'exp': time.time() + exp_time,
        'params': p
    }

    token = jwt.encode(payload, EKEY, algorithm='HS256')

    return token


def validate_teacher_token(tk: str) -> dict:

    try:
        payload = jwt.decode(tk, EKEY, algorithms='HS256')

        if time.time() > payload['exp']:
            return {"error": "Token has expired."}

        params = payload['params']
        id = params.get('id')
        teacher = get_user_by_id(id)

        if teacher == {}:
            return {"error": "User not found."}

        return {"token": tk, "message": "Token is valid."}

    except jwt.ExpiredSignatureError:
        return {"error": "Token has expired."}
    
    except jwt.InvalidTokenError:
        return {"error": "Invalid token."}


def validate_url_token(tk: str) -> dict:

    try:
        payload = jwt.decode(tk, EKEY, algorithms='HS256')

        if time.time() > payload['exp']:
            return {"error": "Token has expired."}

        return {"token": tk, "message": "Token is valid."}

    except jwt.ExpiredSignatureError:
        return {"error": "Token has expired."}
    
    except jwt.InvalidTokenError:
        return {"error": "Invalid token."}