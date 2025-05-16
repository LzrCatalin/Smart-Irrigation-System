import logging

from firebase_admin import db

from src.classes.IrrigationHistory import IrrigationHistory
from src.services.fields_service import get_field_by_id

#######################
#
#   Database path for irrigation history
#
#######################
DB_REF = 'irrigation-system/irrigation_history'
REF = db.reference(f'{DB_REF}')

def get_field_history(field_id: str) -> IrrigationHistory:
	get_field_by_id(field_id)

	snapshot = REF.child(field_id).get()
	if snapshot is not None:
		snapshot['field_id'] = field_id
		return IrrigationHistory.from_dict(snapshot)
	
	return None
	
#######################
#
#   CRUD Operations
#
#######################
def add_irrigation(field_id: str) -> dict:
	try:
		get_field_by_id(field_id)

		# Get existing irrigation or initialize
		snapshot = REF.child(field_id).get()

		if snapshot:
			snapshot['field_id'] = field_id
			history = IrrigationHistory.from_dict(snapshot)

		else:
			history = IrrigationHistory(field_id)

		# Add new timestamp
		history.add_entry()
		
		# Save
		REF.child(field_id).set(history.to_dict())
		return {"status": "success", "field history": history.to_dict()}
	
	except Exception as e:
		logging.error(f"History update failed: {str(e)}")
		raise