from datetime import datetime

class Temperature:
    def __init__(self, thermometer_id: str, nickname: str, current_temp: float, timestamp: datetime):
        self.thermometer_id = thermometer_id
        self.nickname = nickname
        self.current_temp = current_temp
        self.timestamp = timestamp
        
    def __repr__(self):
        return (
            f"Temperature(id={self.id!r}, nickname={self.nickname!r}, "
            f"current_temp={self.current_temp!r}, timestamp={self.timestamp!r})"
        )
