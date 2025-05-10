import os
import time
import jwt
from src.services.users_service import get_user_by_id
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Define
EXPIRE_TOKEN = 'Token has expired.'
INVALID_TOKEN = 'Token is valid.'

key = os.getenv('EKEY')
def generate_token(p: dict, exp_time=3600) -> str:

	payload = {
		'iat': time.time(),
		'exp': time.time() + exp_time,
		'params': p
	}

	token = jwt.encode(payload, key, algorithm='HS256')

	return token


def validate_token(tk: str) -> dict:

	try:
		payload = jwt.decode(tk, key, algorithms='HS256')

		if time.time() > payload['exp']:
			return {"error": EXPIRE_TOKEN}

		params = payload['params']
		user_id = params.get('id')
		user = get_user_by_id(user_id)

		if user == {}:
			return {"error": "User not found."}

		return {"token": tk, "message": INVALID_TOKEN}

	except jwt.ExpiredSignatureError:
		return {"error": EXPIRE_TOKEN}
	
	except jwt.InvalidTokenError:
		return {"error": INVALID_TOKEN}


def validate_url_token(tk: str) -> dict:

	try:
		payload = jwt.decode(tk, key, algorithms='HS256')

		if time.time() > payload['exp']:
			return {"error": EXPIRE_TOKEN}

		return {"token": tk, "message": INVALID_TOKEN}

	except jwt.ExpiredSignatureError:
		return {"error": EXPIRE_TOKEN}
	
	except jwt.InvalidTokenError:
		return {"error": INVALID_TOKEN}