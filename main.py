
import asyncio
from datetime import datetime
import logging

from midea_beautiful import LanDevice
from models.status import Status
from models.temperature import Temperature
from services.firestore_service import add_temperature_to_history, get_active_times, get_firestore, get_status, set_state_by_script
from services.midea_service import change_state_of_appliance, get_appliance_by_id, get_appliances
from services.tapo_service import get_tapo_devices, get_temp_meter_by_id
from utils.envs import load_appliance_ids, load_credentials, load_temp_meter_ids
from utils.log import setup_logging

async def main():
    """Main function to control specific appliances."""
    setup_logging()

    midea_email, midea_password, tapo_email, tapo_password = load_credentials()
    living_room_appliance_id, bedroom_appliance_id, office_appliance_id, attic_appliance_id = load_appliance_ids()
    living_room_temp_meter_id, bedroom_temp_meter_id, office_temp_meter_id, attic_temp_meter_id  = load_temp_meter_ids()

    db = get_firestore()
    status = get_status(db)
    active_times_list = get_active_times(db)
    active = active_times_list.get_active()
    target_temperature = 0
    turn_on_threshold = 99
    if(not status.is_active):
        logging.info(f"Service is not active, returning...")
        active = None
    elif (active is not None): 
        target_temperature = active.max_temp
        turn_on_threshold = active.min_temp

    appliances = get_appliances(midea_email, midea_password)
    living_room_appliance = get_appliance_by_id(appliances, living_room_appliance_id)

    tapo_devices = await get_tapo_devices(tapo_email, tapo_password)
    living_room_temp_meter = get_temp_meter_by_id(tapo_devices, living_room_temp_meter_id)

    check_temperature_for_appliance(
        living_room_appliance,
        living_room_temp_meter, 
        living_room_temp_meter.nickname, 
        target_temperature, 
        turn_on_threshold,
        active,
        status,
        db,
    )
    temperature = Temperature(
        thermometer_id=living_room_temp_meter_id,
        nickname=living_room_temp_meter.nickname,
        current_temp=living_room_temp_meter.current_temperature,
        timestamp=datetime.now()
    )
    add_temperature_to_history(db, temperature)

def check_temperature_for_appliance(
        appliance: LanDevice | None, 
        temp_meter, location: str, 
        target_temperature, 
        turn_on_threshold,
        active,
        status: Status,
        db,
    ):
    current_temperature = temp_meter.current_temperature
    current_state = appliance.state.running
    if(active is None):
        logging.info(f"Not between active times or turned off, returning...")
        if(current_state and status.state_by_script):
            logging.info(f"Powering off device.")
            change_state_of_appliance(appliance, False)
        return

    logging.info(f"Current temperature: {current_temperature} at: {location}")
    if (current_temperature <= turn_on_threshold and current_state == False):
        logging.info(f"Did not reach turn on threshold: {turn_on_threshold}")
        change_state_of_appliance(appliance, True)
        set_state_by_script(db, True)
    elif (current_temperature > target_temperature and current_state == True):
        logging.info(f"Exceeded target temperature: {target_temperature}")
        change_state_of_appliance(appliance, False)
        set_state_by_script(db, False)

if __name__ == "__main__":
    asyncio.run(main())

