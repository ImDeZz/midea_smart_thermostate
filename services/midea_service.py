from midea_beautiful import LanDevice, find_appliances

def get_appliances(email, password, appname="MSmartHome") -> list[LanDevice]:
    """Find and return all appliances associated with the account."""
    appliances = find_appliances(account=email, password=password, appname=appname)

    logging.info(f"Found appliances count: {appliances.__len__()}")
    return appliances

                
def get_appliance_by_id(appliances: list[LanDevice], appliance_id: str):
    """
    Retrieve an appliance by its ID from a list of appliances.

    Args:
        appliances (list): A list of appliance objects.
        appliance_id (str): The ID of the appliance to find.

    Returns:
        Appliance: The appliance object with the matching ID, or None if not found.
    """
    for appliance in appliances:
        if appliance.state.appliance_id == appliance_id:
            logging.info(f"Found appliance with id: {appliance_id}")
            return appliance
    return None


def change_state_of_appliance(appliance: LanDevice, state: bool):
    """
    Change the running state of an appliance.

    Args:
        appliance: The appliance object to modify.
        state (bool): True to turn the appliance on, False to turn it off.

    Returns:
        None
    """
    appliance.state.running = state
    appliance.apply()
    state_text = "ON" if state else "OFF"
    logging.info(f"{appliance.name!r} is now turned {state_text}.")
