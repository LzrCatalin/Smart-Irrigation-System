import logging
from colorama import Fore, Style
from firebase_admin import db

from src.classes.UserAlerts import UserAlerts
from src.classes.AlertDefinition import AlertDefinition
from src.services.users_service import get_user_by_id
#######################
#
#   Database path for alerts
#
#######################
DB_REF = 'irrigation-system/user_alerts'
REF = db.reference(f'{DB_REF}')

def get_user_alerts(user_id: str) -> UserAlerts:
	"""Helper to fetch existing alerts"""
	snapshot = REF.child(user_id).get()
	
	return UserAlerts.from_dict(snapshot) if snapshot else None

#######################
#
#   CRUD Operations
#
#######################
def create_alert(alert_def: AlertDefinition) -> None:
	try:
		user_ref = REF.child(alert_def.user_id)
		
		# Get existing data or initialize
		user_ref.get() or {"alerts": {}}
		
		# Create safe timestamp key
		safe_timestamp = alert_def.timestamp.replace(':', '-').replace('.', '-')
		
		# Prepare update
		updates = {
			f"alerts/{safe_timestamp}/message": alert_def.message,
			f"alerts/{safe_timestamp}/type": alert_def.alert_type
		}
		
		# Atomic update
		user_ref.update(updates)
		
	except Exception as e:
		logging.error(f"Alert creation failed: {str(e)}")
		raise