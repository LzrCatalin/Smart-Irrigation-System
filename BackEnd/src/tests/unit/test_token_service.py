import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../')))

import pytest
import jwt
import time
from unittest.mock import patch
from src.services.token_service import generate_token, validate_token, validate_url_token, EXPIRE_TOKEN, INVALID_TOKEN

# Sample user payload
sample_payload = {"id": "user_123"}

# Patch environment variable for JWT key
@pytest.fixture(scope="module", autouse=True)
def patch_env_key(monkeypatch):
	monkeypatch.setenv("EKEY", "testsecret")


# --- Positive Tests ---

def test_generate_and_validate_token(monkeypatch):
	# Mock user service to always return a valid user
	monkeypatch.setattr("src.util.token_service.get_user_by_id", lambda uid: {"id": uid, "email": "test@example.com"})

	token = generate_token(sample_payload, exp_time=3)
	result = validate_token(token)

	assert result["token"] == token
	assert result["message"] == INVALID_TOKEN

def test_validate_url_token_valid():
	token = generate_token(sample_payload, exp_time=3)
	result = validate_url_token(token)

	assert result["token"] == token
	assert result["message"] == INVALID_TOKEN

# --- Negative Tests ---

def test_validate_token_expired(monkeypatch):
	monkeypatch.setattr("src.util.token_service.get_user_by_id", lambda uid: {"id": uid})

	# Create token with very short expiry
	token = generate_token(sample_payload, exp_time=1)
	time.sleep(2)

	result = validate_token(token)
	assert result["error"] == EXPIRE_TOKEN

def test_validate_url_token_expired():
	token = generate_token(sample_payload, exp_time=1)
	time.sleep(2)

	result = validate_url_token(token)
	assert result["error"] == EXPIRE_TOKEN

def test_validate_token_invalid(monkeypatch):
	monkeypatch.setattr("src.util.token_service.get_user_by_id", lambda uid: {"id": uid})
	# Corrupt token
	corrupted_token = "invalid.token.value"

	result = validate_token(corrupted_token)
	assert result["error"] == INVALID_TOKEN

def test_validate_token_user_not_found(monkeypatch):
	# User not found (empty dict)
	monkeypatch.setattr("src.util.token_service.get_user_by_id", lambda uid: {})
	token = generate_token(sample_payload, exp_time=5)

	result = validate_token(token)
	assert result["error"] == "User not found."
