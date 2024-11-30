import logging
from tapo import ApiClient

async def get_tapo_devices(email: str, password: str):
    client = ApiClient(email, password)
    ip = '192.168.100.71' # TODO: Get this from the Firestore
    logging.info(f"Connecting to hub at: {ip}")
    hub = await client.h100(ip)
    child_device_list = await hub.get_child_device_list()
    logging.info(f"Got child devices: {child_device_list}")
    return child_device_list

def get_temp_meter_by_id(devices, device_id):
    for device in devices:
        if (device.device_id == device_id):
            logging.info(f"Found device with Id: {device_id}")
            return device
    
