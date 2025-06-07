import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../')))

import pytest
from unittest.mock import patch, MagicMock
from src.services.users_service import get_user_by_id, available_email

# ✅ Positive test: valid user ID, returns correct user data
@patch("src.services.users_service.db.reference")
def test_get_user_by_id_success(mock_db_ref):
	mock_child = MagicMock()
	mock_child.get.return_value = {"email": "test@example.com"}
	mock_db_ref.return_value.child.return_value = mock_child

	result = get_user_by_id("1234")
	assert result == {"id": "1234", "email": "test@example.com"}

# ✅ Test user ID does not exist
@patch("src.services.users_service.db.reference")
def test_get_user_by_id_not_found(mock_db_ref):
	mock_child = MagicMock()
	mock_child.get.return_value = None
	mock_db_ref.return_value.child.return_value = mock_child

	result = get_user_by_id("nonexistent")
	assert result == {"error": "No data found for ID: nonexistent"}

# ✅ Test user data is missing expected 'email' key
@patch("src.services.users_service.db.reference")
def test_get_user_by_id_missing_email(mock_db_ref):
	mock_child = MagicMock()
	mock_child.get.return_value = {"wrong_key": "value"}
	mock_db_ref.return_value.child.return_value = mock_child

	result = get_user_by_id("1234")
	assert result == {"error": "Key missing: 'email'"}

# ❌ Test returns a wrong expected email
@patch("src.services.users_service.db.reference")
def test_get_user_by_id_wrong_output(mock_db_ref):
	mock_child = MagicMock()
	mock_child.get.return_value = {"email": "wrong@example.com"}
	mock_db_ref.return_value.child.return_value = mock_child

	result = get_user_by_id("1234")

	# This is intentionally wrong → should FAIL ❌
	assert result == {"id": "1234", "email": "notwhatweexpect@example.com"}

# ✅ Test available_email returns False when email already exists
@patch("src.services.users_service.db.reference")
def test_available_email_should_be_false(mock_db_ref):
	mock_ref = MagicMock()
	mock_ref.get.return_value = {
		"uid1": {"email": "existing@example.com"}
	}
	mock_db_ref.return_value = mock_ref

	result = available_email("existing@example.com")
	assert result is False

# ❌ Test expects True when email already exists
@patch("src.services.users_service.db.reference")
def test_available_email_wrong_expectation(mock_db_ref):
	mock_ref = MagicMock()
	mock_ref.get.return_value = {
		"uid1": {"email": "existing@example.com"}
	}
	mock_db_ref.return_value = mock_ref

	result = available_email("existing@example.com")

	# This is intentionally wrong → should FAIL ❌
	assert result is True
