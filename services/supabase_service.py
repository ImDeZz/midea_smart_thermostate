from datetime import datetime
import logging
from models.active_time import ActiveTime, ActiveTimeList
from models.status import Status
from supabase import create_client, Client
import os

from models.temperature import Temperature

# Example: Insert a new row into a "users" table
def get_supabase_client(url, key):
    supabase: Client = create_client(url, key)
    return supabase
    

def get_thermometer_id(db: Client, thermometer_id: str) -> int:
    response = db.table('thermometer').select('*').filter('thermometer_id', 'eq', thermometer_id).execute()
    response_data = response.data
    return response_data[0]['id']


def get_active_times(db: Client, thermometer_id: int) -> ActiveTimeList:
    try:
        # Fetch the document from Firestore
        response = db.table('active_times').select('*').filter('thermometer_id', 'eq', thermometer_id).execute()
        
        active_time_list = ActiveTimeList()
        for item in response.data:
            active_time = ActiveTime(
                start_time=item["start_time"],
                end_time=item["end_time"],
                day=item["day"],
                min_temp=item["min_temp"],
                max_temp=item["max_temp"]
            )
            active_time_list.add_active_time(active_time)

        logging.info(f"Loaded active times: {active_time_list}")
        return active_time_list

    except Exception as e:
        logging.error(f"Failed to fetch or parse active times from Firestore: {e}")
        return None


def get_status(db: Client, thermometer_id: int) -> Status:
    response = db.table('status').select('*').filter('thermometer_id', 'eq', thermometer_id).execute()
    print(f"{response.data}")
    status = Status(
        is_active=True,
        state_by_script=True,
        state_by_script_date=""
    )

    logging.info(f"Status: {status}")
    
    return status


def add_temperature_to_history(db: Client, temperature: Temperature):
    temperature_data = {
        "thermometer_id": temperature.thermometer_id,
        "nickname": temperature.nickname,
        "current_temp": temperature.current_temp,
    }

    # Add to Firestore collection
    db.table('history').insert(temperature_data).execute()
    logging.info(f"Temperature data added to history: {temperature_data}")
    return True


def set_state_by_script(db: Client, state: bool, thermometer_id: int):
    db.table('status').update({
        "state_by_script": state,
        "state_by_script_date": datetime.now()
    }).filter('thermometer_id', 'eq', thermometer_id).execute()
    logging.info(f"State set by script: {state}")

def get_state_by_script(db: Client): 
    return False