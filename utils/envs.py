from dotenv import load_dotenv
import os

def load_credentials():
    """Load credentials from environment variables."""
    load_dotenv()
    midea_email = os.getenv("MIDEA_EMAIL")
    midea_password = os.getenv("MIDEA_PASSWORD")
    tapo_email = os.getenv("TAPO_EMAIL")
    tapo_password = os.getenv("TAPO_PASSWORD")
    return midea_email, midea_password, tapo_email, tapo_password

def load_appliance_ids():
    """Load IDs from environment variables."""
    load_dotenv()
    living_room_appliance_id = os.getenv("LIVING_ROOM_APPLIANCE_ID")
    bedroom_appliance_id = os.getenv("BEDROOM_APPLIANCE_ID")
    office_appliance_id = os.getenv("OFFICE_APPLIANCE_ID")
    attic_appliance_id = os.getenv("ATTIC_APPLIANCE_ID")
    return living_room_appliance_id, bedroom_appliance_id, office_appliance_id, attic_appliance_id 

def load_temp_meter_ids():
    """Load IDs from environment variables."""
    load_dotenv()
    living_room_temp_meter_id = os.getenv("LIVING_ROOM_TEMP_METER_ID")
    bedroom_temp_meter_id = os.getenv("BEDROOM_TEMP_METER")
    office_temp_meter_id = os.getenv("OFFICE_TEMP_METER")
    attic_temp_meter_id = os.getenv("ATTIC_TEMP_METER")
    return living_room_temp_meter_id, bedroom_temp_meter_id, office_temp_meter_id, attic_temp_meter_id 

def load_supabase_vars():
    """Load Supabase vars from environment variables."""
    load_dotenv()
    supabase_url = os.getenv("SUPABASE_URL")
    supabase_key = os.getenv("SUPABASE_KEY")
    return supabase_url, supabase_key
