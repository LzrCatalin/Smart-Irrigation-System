from datetime import datetime
from typing import Dict

from src.classes.AlertDefinition import AlertDefinition

class UserAlerts:
	def __init__(self, user_id: str, existing_alerts: Dict[str, Dict] = None) -> None:
		self.user_id = user_id
		self.alerts = existing_alerts if existing_alerts else {}


	def add_alert(self, alert_def: AlertDefinition) -> str:
		safe_timestamp = alert_def.timestamp.replace(':', '-').replace('.', '-')
		self.alerts[safe_timestamp] = {
			"message": alert_def.message,
			"type": alert_def.alert_type
		}
		return safe_timestamp
	
	def to_dict(self) -> Dict:
		return {
			"user_id": self.user_id,
			"alerts": self.alerts
		}
	
	@staticmethod
	def from_dict(data: dict) -> "UserAlerts":
		return UserAlerts(
			user_id=data["user_id"],
			existing_alerts=data.get("alerts", {})
		)