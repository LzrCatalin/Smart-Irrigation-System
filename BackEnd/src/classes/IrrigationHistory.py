from datetime import datetime
from typing import Dict, List

class IrrigationHistory:
	def __init__(self, field_id: str, existing_irrigations: List[str] = None) -> None:
		self.field_id = field_id
		self.history = existing_irrigations if existing_irrigations else []

	def add_entry(self) -> str:
		timestamp = datetime.now().isoformat().replace(':', '-').replace('.', '-')
		self.history.append(timestamp)
		return timestamp
	
	def to_dict(self) -> Dict:
		return {
			"history": self.history
		}
	
	@staticmethod
	def from_dict(data: dict) -> "IrrigationHistory":
		return IrrigationHistory(
			field_id=data["field_id"],
			existing_irrigations=data.get("history", [])
		)