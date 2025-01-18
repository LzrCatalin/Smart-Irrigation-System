import hashlib
import random
import string

#########################
#
#	User Password Encryption
#
#########################
def encrypt(password: str) -> str:
	sha256 = hashlib.sha256()
	sha256.update(password.encode('utf-8'))
	return to_hex_string(sha256.digest())


def to_hex_string(hash_bytes: bytes) -> str:
	hex_string = hash_bytes.hex()
	return hex_string.zfill(64)


def generate_random_password(length=10) -> str:
	all_characters = string.ascii_letters + string.digits + string.punctuation
	password = ''.join(random.choice(all_characters) for _ in range(length))
	return password