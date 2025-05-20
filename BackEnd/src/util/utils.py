from src.classes.AlertDefinition import AlertDefinition
from src.services.alerts_service import create_alert

def alert(user_id: str, message: str, type: str):
	alert_def = AlertDefinition(
		user_id=user_id,
		message=message,
		alert_type=type
	)

	create_alert(alert_def)