import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../')))

import pytest
from unittest.mock import patch, MagicMock
from src.services.alerts_service import get_user_alerts, create_alert
from src.classes.AlertDefinition import AlertDefinition

# ✅ Test: successful retrieval of user alerts
@patch("src.services.alerts_service.get_user_by_id")
@patch("src.services.alerts_service.db.reference")
def test_get_user_alerts_success(mock_db_ref, mock_get_user_by_id):
    # Simulate alert data stored in Firebase
    mock_alert_data = {
        "alerts": {
            "2024-06-06T12-00-00": {
                "message": "Irrigation started",
                "type": "INFO"
            }
        }
    }

    mock_ref = MagicMock()
    mock_ref.child.return_value.get.return_value = mock_alert_data
    mock_db_ref.return_value = mock_ref

    result = get_user_alerts("user123")

    # Check that alerts were correctly parsed
    assert result.user_id == "user123"
    assert "2024-06-06T12-00-00" in result.alerts
    assert result.alerts["2024-06-06T12-00-00"].message == "Irrigation started"
    assert result.alerts["2024-06-06T12-00-00"].alert_type == "INFO"

# ❌ Test: expected to fail - missing alert key
@patch("src.services.alerts_service.get_user_by_id")
@patch("src.services.alerts_service.db.reference")
def test_get_user_alerts_should_fail_on_wrong_key(mock_db_ref, mock_get_user_by_id):
    mock_alert_data = {
        "bad_key": {
            "message": "This should not be here",
            "type": "ERROR"
        }
    }

    mock_ref = MagicMock()
    mock_ref.child.return_value.get.return_value = mock_alert_data
    mock_db_ref.return_value = mock_ref

    result = get_user_alerts("user123")

    # This should fail because "bad_key" is not a valid timestamp key
    assert "alerts" in result.alerts  # This will raise AttributeError or fail logically

# ✅ Test: create alert successfully with formatted timestamp
@patch("src.services.alerts_service.db.reference")
def test_create_alert_success(mock_db_ref):
    mock_user_ref = MagicMock()
    mock_user_ref.get.return_value = {"alerts": {}}
    mock_db_ref.return_value.child.return_value = mock_user_ref

    alert_def = AlertDefinition(
        user_id="user123",
        timestamp="2024-06-06T12:00:00",
        message="Soil too dry",
        alert_type="CRITICAL"
    )

    create_alert(alert_def)

    # Timestamp should be safely formatted
    safe_ts = "2024-06-06T12-00-00"
    expected_updates = {
        f"alerts/{safe_ts}/message": "Soil too dry",
        f"alerts/{safe_ts}/type": "CRITICAL"
    }

    mock_user_ref.update.assert_called_once_with(expected_updates)

# ❌ Test: expected to fail - missing user_id in alert definition
def test_create_alert_should_fail_missing_user_id():
    # AlertDefinition missing required `user_id` field -> should raise TypeError
    with pytest.raises(TypeError):
        create_alert(AlertDefinition(
            timestamp="2024-06-06T12:00:00",
            message="Bad alert",
            alert_type="ERROR"
        ))
