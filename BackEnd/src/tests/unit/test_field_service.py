import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../')))

import pytest
from unittest.mock import patch, MagicMock
from src.services.fields_service import (
	get_field_by_id,
	get_field_ids_with_sensors
)

# ✅ Test: get_field_by_id returns valid FieldDTO when field exists
@patch("src.services.fields_service.db.reference")
def test_get_field_by_id_success(mock_db_ref):
	# Mock the Firebase call
	mock_ref = MagicMock()
	mock_ref.child.return_value.get.return_value = {
		"latitude": 45.1,
		"longitude": 21.2,
		"width": 50,
		"length": 80,
		"slope": 5,
		"user": "user123",
		"soil_type": "sandy",
		"crop_name": "corn",
		"sensors": []
	}
	mock_db_ref.return_value = mock_ref

	result = get_field_by_id("field123")

	# Assertions on DTO structure
	assert result["id"] == "field123"
	assert result["latitude"] == 45.1
	assert result["crop_name"] == "corn"

# ❌ Test: should fail when required field key is missing
@patch("src.services.fields_service.db.reference")
def test_get_field_by_id_missing_key_should_fail(mock_db_ref):
	# 'crop_name' is missing
	mock_ref = MagicMock()
	mock_ref.child.return_value.get.return_value = {
		"latitude": 45.1,
		"longitude": 21.2,
		"width": 50,
		"length": 80,
		"slope": 5,
		"user": "user123",
		"soil_type": "sandy",
		"sensors": []
	}
	mock_db_ref.return_value = mock_ref

	result = get_field_by_id("field123")

	# This will return an error dict
	assert "error" in result

# ✅ Test: get_field_ids_with_sensors filters correctly only fields with sensors
@patch("src.services.fields_service.db.reference")
def test_get_field_ids_with_sensors_success(mock_db_ref):
	# Mock database structure
	mock_db_ref.return_value.get.return_value = {
		"field1": {"sensors": {"s1": True}},
		"field2": {"sensors": {}},
		"field3": {},
		"field4": {"sensors": {"s2": True, "s3": True}},
	}

	result = get_field_ids_with_sensors()

	# Should return only fields that have non-empty 'sensors'
	assert sorted(result) == ["field1", "field4"]

# ❌ Test: expected to fail due to invalid assumption
@patch("src.services.fields_service.db.reference")
def test_get_field_ids_with_sensors_should_fail_invalid_structure(mock_db_ref):
	# None of these fields have sensors
	mock_db_ref.return_value.get.return_value = {
		"field1": {},
		"field2": {},
		"field3": {}
	}

	result = get_field_ids_with_sensors()

	# Intentionally incorrect: we assert a result we know is wrong
	assert result == ["field1"]  # This should fail
