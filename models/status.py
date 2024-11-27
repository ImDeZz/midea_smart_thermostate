from datetime import datetime
from google.cloud import firestore

class Status:
    def __init__(self, is_active: bool, state_by_script: bool, state_by_script_date: datetime = firestore.SERVER_TIMESTAMP):
        self.is_active = is_active
        self.state_by_script = state_by_script
        self.state_by_script_date = state_by_script_date
        
    def __repr__(self):
        return (
            f"Status(is_active={self.is_active!r}, state_by_script={self.state_by_script!r}, "
            f"state_by_script_date={self.state_by_script_date!r})"
        )