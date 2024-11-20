
import asyncio
import logging

from midea_beautiful import LanDevice
from services.firestore_service import get_firestore, get_thresholds
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
    target_temperature, turn_on_threhold = get_thresholds(db)
    
    appliances = get_appliances(midea_email, midea_password)
    living_room_appliance = get_appliance_by_id(appliances, living_room_appliance_id)

    tapo_devices = await get_tapo_devices(tapo_email, tapo_password)
    living_room_temp_meter = get_temp_meter_by_id(tapo_devices, living_room_temp_meter_id)

    check_temperature_for_appliance(
        living_room_appliance,
        living_room_temp_meter, 
        'Nappali', 
        target_temperature, 
        turn_on_threhold
    )

def check_temperature_for_appliance(
        appliance: LanDevice | None, 
        temp_meter, location: str, 
        target_temperature, 
        turn_on_threshold
    ):
    current_temperature = temp_meter.current_temperature
    current_state = appliance.state.running
    logging.info(f"Current temperature: {current_temperature} at: {location}")
    if (current_temperature <= turn_on_threshold and current_state == False):
        logging.info(f"Did not reach turn on threshold: {turn_on_threshold}")
        change_state_of_appliance(appliance, True)
    elif (current_temperature > target_temperature and current_state == True):
        logging.info(f"Exceeded target temperature: {target_temperature}")
        change_state_of_appliance(appliance, False)

if __name__ == "__main__":
    asyncio.run(main())
