import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../')))

import pytest
from unittest.mock import patch, MagicMock
from src.services.history_service import get_field_history, add_irrigation

# ✅ Test: get_field_history returns IrrigationHistory with correct field_id
@patch("src.services.history_service.get_field_by_id")
@patch("src.services.history_service.db.reference")
def test_get_field_history_success(mock_db_ref, mock_get_field):
	mock_snapshot = {
		"history": ["2024-06-01T10:00:00"]
	}

	mock_ref = MagicMock()
	mock_ref.child.return_value.get.return_value = mock_snapshot
	mock_db_ref.return_value = mock_ref

	result = get_field_history("field123")

	assert result.field_id == "field123"
	assert "2024-06-01T10:00:00" in result.history

# ❌ Test: get_field_history fails due to malformed snapshot (missing 'history')
@patch("src.services.history_service.get_field_by_id")
@patch("src.services.history_service.db.reference")
def test_get_field_history_invalid_data_should_fail(mock_db_ref, mock_get_field):
	# Simulate invalid Firebase data
	mock_snapshot = {
		"wrong_key": "unexpected"
	}

	mock_ref = MagicMock()
	mock_ref.child.return_value.get.return_value = mock_snapshot
	mock_db_ref.return_value = mock_ref

	# This will fail because IrrigationHistory.from_dict will not find 'history'
	result = get_field_history("field123")

	assert result is None or "history" in result.history  # This fails

# ✅ Test: add_irrigation adds entry and writes to Firebase
@patch("src.services.history_service.get_field_by_id")
@patch("src.services.history_service.db.reference")
def test_add_irrigation_success(mock_db_ref, mock_get_field):
	mock_ref = MagicMock()
	mock_ref.child.return_value.get.return_value = {
		"history": ["2024-06-01T10:00:00"]
	}
	mock_db_ref.return_value = mock_ref

	response = add_irrigation("field123")

	assert response["status"] == "success"
	assert "field history" in response

# ❌ Test: add_irrigation fails if REF is not defined
@patch("src.services.history_service.get_field_by_id")
@patch("src.services.history_service.db.reference")
def test_add_irrigation_should_fail_missing_ref(mock_db_ref, mock_get_field):
	# Simulate REF is undefined (we'll bypass get_ref and use REF directly)
	from src.services import history_service
	history_service.REF = None  # Intentionally break it

	with pytest.raises(AttributeError):
		add_irrigation("field123")
