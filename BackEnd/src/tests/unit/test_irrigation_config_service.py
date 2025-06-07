import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../')))

import pytest
from unittest.mock import patch, MagicMock
from src.services.irrigation_config_service import (
	push_into_system,
	remove_from_system,
	update_field_irrigation_config,
	toggle_scheduler_activity,
	toggle_irrigation_activity,
	update_sensors_interval,
	update_irrigation_interval
)

# ✅ Test push_into_system with valid field
@patch("src.services.irrigation_config_service.get_irrigation_system")
@patch("src.services.irrigation_config_service.get_field_by_id")
@patch("src.services.irrigation_config_service.get_field_user")
@patch("src.services.irrigation_config_service.alert")
def test_push_into_system(mock_alert, mock_get_field_user, mock_get_field_by_id, mock_get_system):
	mock_get_system.return_value = MagicMock(add_field=MagicMock())
	mock_get_field_user.return_value = "userX"
	mock_get_field_by_id.return_value = {"crop_name": "corn"}

	result = push_into_system("field123")

	assert result == {"message": "OK"}
	mock_alert.assert_called_once()

# ❌ Test push_into_system expecting error but input is valid (fails intentionally)
@patch("src.services.irrigation_config_service.get_irrigation_system")
@patch("src.services.irrigation_config_service.get_field_by_id")
@patch("src.services.irrigation_config_service.get_field_user")
@patch("src.services.irrigation_config_service.alert")
def test_push_into_system_should_fail(mock_alert, mock_get_field_user, mock_get_field_by_id, mock_get_system):
	mock_get_system.return_value = MagicMock(add_field=MagicMock())
	mock_get_field_user.return_value = "userX"
	mock_get_field_by_id.return_value = {"crop_name": "corn"}

	result = push_into_system("field123")

	assert result == {"error": "Job failed"}  # ❌ incorrect expectation

# ✅ Test toggle_scheduler_activity pause
@patch("src.services.irrigation_config_service.get_sensors_scheduler")
@patch("src.services.irrigation_config_service.alert")
def test_toggle_scheduler_activity_pause(mock_alert, mock_get_scheduler):
	scheduler_mock = MagicMock()
	mock_get_scheduler.return_value = scheduler_mock

	result = toggle_scheduler_activity({"state": 1, "user_id": "u1"})
	assert result == {"message": "Scheduler paused"}
	scheduler_mock.pause_sensor_updates.assert_called_once()

# ✅ Test update_field_irrigation_config happy path
@patch("src.services.irrigation_config_service.send_email")
@patch("src.services.irrigation_config_service.generate_field_config_update")
@patch("src.services.irrigation_config_service.get_irrigation_system")
@patch("src.services.irrigation_config_service.get_location")
@patch("src.services.irrigation_config_service.get_user_by_id")
@patch("src.services.irrigation_config_service.get_field_by_id")
@patch("src.services.irrigation_config_service.alert")
def test_update_field_irrigation_config_success(mock_alert, mock_get_field, mock_get_user, mock_location, mock_get_sys, mock_gen_mail, mock_send_mail):
	mock_get_field.return_value = {"crop_name": "Tomato", "latitude": 45, "longitude": 25}
	mock_get_user.return_value = {"email": "test@example.com"}
	mock_location.return_value = "Location:Test"
	mock_get_sys.return_value = MagicMock(update_field_config=MagicMock())

	data = {
		"fieldId": "f123",
		"userId": "u456",
		"min_humidity": 10,
		"target_humidity": 60,
		"max_watering_time": 20
	}

	result = update_field_irrigation_config(data)
	assert result == {"message": "Field f123 config updated."}
	mock_alert.assert_called_once()
	mock_send_mail.assert_called_once()

# ❌ Test update_irrigation_interval fails due to wrong return
@patch("src.services.irrigation_config_service.get_irrigation_system")
@patch("src.services.irrigation_config_service.alert")
def test_update_irrigation_interval_wrong_return(mock_alert, mock_get_sys):
	mock_get_sys.return_value = MagicMock(
		pause_irrigation_system=MagicMock(),
		update_interval=MagicMock()
	)
	data = {"interval": 10, "user_id": "u123"}
	result = update_irrigation_interval(data)

	assert result == {"message": "Fail expected"}  # ❌ This will fail
