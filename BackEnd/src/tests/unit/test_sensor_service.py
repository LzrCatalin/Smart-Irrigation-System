import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../')))

import pytest
from unittest.mock import patch, MagicMock
from src.services.sensors_services import (
	get_sensor_data_by_id,
	get_sensors_ids,
	get_sensors_data_by_type,
	set_sensor_field_id
)

# ✅ Test: get_sensor_data_by_id returns DTO when data exists
@patch("src.services.sensors_services.db.reference")
def test_get_sensor_data_by_id_success(mock_db_ref):
	mock_ref = MagicMock()
	mock_ref.child.return_value.get.return_value = {
		"name": "sensor1",
		"type": {"type": "HUMIDITY", "port": 1, "status": "AVAILABLE"},
		"field_id": "none"
	}
	mock_db_ref.return_value = mock_ref

	result = get_sensor_data_by_id("s123")

	assert result["id"] == "s123"
	assert result["name"] == "sensor1"
	assert result["field_id"] == "none"

# ❌ Test: get_sensor_data_by_id fails with missing key
@patch("src.services.sensors_services.db.reference")
def test_get_sensor_data_by_id_missing_key_should_fail(mock_db_ref):
	mock_ref = MagicMock()
	mock_ref.child.return_value.get.return_value = {
		# Missing 'name'
		"type": {"type": "HUMIDITY", "port": 1, "status": "AVAILABLE"},
		"field_id": "none"
	}
	mock_db_ref.return_value = mock_ref

	result = get_sensor_data_by_id("s123")

	# This will return None due to KeyError
	assert result is not None  # ❌ Intentionally wrong

# ✅ Test: get_sensors_ids returns list of IDs
@patch("src.services.sensors_services.db.reference")
def test_get_sensors_ids_success(mock_db_ref):
	mock_db_ref.return_value.get.return_value = {
		"s1": {}, "s2": {}, "s3": {}
	}

	result = get_sensors_ids()
	assert sorted(result) == ["s1", "s2", "s3"]

# ❌ Test: get_sensors_ids should fail if we expect incorrect value
@patch("src.services.sensors_services.db.reference")
def test_get_sensors_ids_should_fail_with_wrong_expectation(mock_db_ref):
	mock_db_ref.return_value.get.return_value = {
		"s1": {}, "s2": {}, "s3": {}
	}

	result = get_sensors_ids()
	assert result == ["s1", "s3"]  # ❌ Incorrect expectation

# ✅ Test: get_sensors_data_by_type filters by type
@patch("src.services.sensors_services.db.reference")
def test_get_sensors_data_by_type_success(mock_db_ref):
	mock_db_ref.return_value.get.return_value = {
		"s1": {"type": {"type": "HUMIDITY"}},
		"s2": {"type": {"type": "TEMP"}},
		"s3": {"type": {"type": "HUMIDITY"}},
	}

	result = get_sensors_data_by_type("HUMIDITY")

	assert "s1" in result
	assert "s3" in result
	assert "s2" not in result

# ✅ Test: set_sensor_field_id correctly updates field_id
@patch("src.services.sensors_services.get_sensor_data_by_id")
@patch("src.services.sensors_services.db.reference")
def test_set_sensor_field_id_success(mock_db_ref, mock_get_sensor):
	mock_sensor = {
		"name": "sensorX",
		"type": {"type": "HUMIDITY", "port": 2, "status": "AVAILABLE"},
		"field_id": "none"
	}

	mock_get_sensor.return_value = mock_sensor
	mock_ref = MagicMock()
	mock_db_ref.return_value.child.return_value = mock_ref

	set_sensor_field_id("s99", "f77")

	mock_sensor["field_id"] = "f77"
	mock_ref.set.assert_called_once_with(mock_sensor)
