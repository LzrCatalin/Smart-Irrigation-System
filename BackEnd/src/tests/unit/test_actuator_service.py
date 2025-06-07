import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../')))

import pytest
from unittest.mock import patch, MagicMock
from src.services.actuators_service import toggle_water_pump

# ✅ Test: Water pump ON
@patch("src.services.pump_service.pump_start")
@patch("src.services.pump_service.add_irrigation")
@patch("src.services.pump_service.get_location_by_field_id")
@patch("src.services.pump_service.alert")
def test_toggle_water_pump_on(mock_alert, mock_get_location, mock_add_irrigation, mock_pump_start):
    mock_get_location.return_value = "RO: Bacau"

    result = toggle_water_pump({
        "state": 1,
        "user_id": "user1",
        "field_id": "field1"
    })

    assert result == {"message": "WATER PUMP -> ON"}

# ✅ Test: Water pump OFF
@patch("src.services.pump_service.pump_stop")
@patch("src.services.pump_service.alert")
def test_toggle_water_pump_off(mock_alert, mock_pump_stop):
    result = toggle_water_pump({
        "state": 0,
        "user_id": "user1",
        "field_id": "field1"
    })

    assert result == {"message": "WATER PUMP -> OFF"}

# ❌ Failing test: wrong expected message
@patch("src.services.pump_service.pump_start")
@patch("src.services.pump_service.add_irrigation")
@patch("src.services.pump_service.get_location_by_field_id")
@patch("src.services.pump_service.alert")
def test_toggle_water_pump_wrong_message(mock_alert, mock_get_location, mock_add_irrigation, mock_pump_start):
    mock_get_location.return_value = "RO: Iasi"

    result = toggle_water_pump({
        "state": 1,
        "user_id": "user1",
        "field_id": "field1"
    })

    # Intentionally expecting incorrect result to verify the test fails
    assert result == {"message": "WATER PUMP -> FAIL"}

# ❌ Failing test: missing 'state' key in input
def test_toggle_water_pump_missing_key():
    with pytest.raises(KeyError):
        # Missing 'state' key should raise a KeyError
        toggle_water_pump({
            "user_id": "user1",
            "field_id": "field1"
        })