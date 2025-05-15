from dataclasses import dataclass
from datetime import datetime
from typing import Dict

@dataclass
class AlertDefinition:
	"""Standardized alert structure"""
	user_id: str
	message: str
	alert_type: str = "INFO" # Default
	timestamp: str = None

	def __post_init__(self):
		"""Auto-generate timestamp if not provided"""
		if self.timestamp is None:
			self.timestamp = datetime.now().isoformat()