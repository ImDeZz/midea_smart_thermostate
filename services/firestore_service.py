import logging
from typing import Optional
import firebase_admin
from firebase_admin import credentials, firestore
from google.cloud.firestore_v1 import Client
import os

from models.active_time import ActiveTime, ActiveTimeList
from models.status import Status
from models.temperature import Temperature

# Get the directory where the script is located
script_dir = os.path.dirname(os.path.realpath(__file__))

# Build the path to the secrets folder
service_account_path = os.path.join(script_dir, "..", "secrets", "midea_smart_thermostate_service_account.json")

# Optionally, print to verify the correct path
logging.info(f"Service account path: {service_account_path}")

# Initialize the Firebase app
def get_firestore() :
    print(f"Accessing : {service_account_path}")
    cred = credentials.Certificate(service_account_path)
    app = firebase_admin.initialize_app(cred)
    print(f"App name: {app.name}")
    print(f"App project id: {app.project_id}")
    # Access Firestore
    db = firestore.client()
    docref = db.collection("data").document("status")
    
    logging.info(f"{docref}")
    doc = docref.get(timeout=7)
    logging.info(f"{doc}")
    logging.info("Firebase connection initialized successfully.")
    return db

def get_active_times(db: Client, document_path: str = "data/active_times") -> Optional[ActiveTimeList]:
    """
    Fetch and deserialize active times from Firestore.

    Args:
        db (Client): Firestore client instance.
        document_path (str): Path to the Firestore document containing active times.

    Returns:
        Optional[ActiveTimeList]: A populated ActiveTimeList object, or None if the document doesn't exist or fails to load.
    """
    try:
        # Fetch the document from Firestore
        doc_ref = db.document(document_path)
        doc = doc_ref.get()

        if not doc.exists:
            logging.warning(f"Document {document_path} does not exist.")
            return None

        # Deserialize the document into ActiveTimeList
        data = doc.to_dict()
        active_time_list = ActiveTimeList()

        for item in data.get("active_times", []):
            active_time = ActiveTime(
                start_time=item.get("start_time"),
                end_time=item.get("end_time"),
                day=item.get("day"),
                min_temp=item.get("min_temp"),
                max_temp=item.get("max_temp")
            )
            active_time_list.add_active_time(active_time)

        logging.info(f"Loaded active times: {active_time_list}")
        return active_time_list

    except Exception as e:
        logging.error(f"Failed to fetch or parse active times from Firestore: {e}")
        return None


def get_status(db: Client) -> Status:
    docref = db.collection("data").document("status")
    
    logging.info(f"{docref}")
    doc = docref.get(timeout=7)
    logging.info(f"{doc}")
    status = Status(
        is_active=doc.get("is_active"),
        state_by_script=doc.get("state_by_script"),
        state_by_script_date=doc.get("state_by_script_date")
    )

    logging.info(f"Status: {status}")
    
    return status


def add_temperature_to_history(db: Client, temperature: Temperature):
    """
    Add a Temperature object to the Firestore temperature history if the service is active.

    Args:
        db (firestore.Client): Firestore client instance.
        temperature (Temperature): The Temperature object to add.

    Returns:
        bool: True if the temperature was added, False otherwise.
    """
    # Check if the service is active
    doc = db.collection("data").document("status").get()
    is_active = doc.get("is_active")

    logging.info(f"Service is active: {is_active}")

    if not is_active:
        logging.warning("Service is inactive. Temperature will not be added.")
        return False

    temperature_data = {
        "thermometer_id": temperature.thermometer_id,
        "nickname": temperature.nickname,
        "current_temp": temperature.current_temp,
        "timestamp": temperature.timestamp
    }

    # Add to Firestore collection
    db.collection("history").add(temperature_data)
    logging.info(f"Temperature data added to history: {temperature_data}")
    return True


def set_state_by_script(db: Client, state: bool):
    db.collection("data").document("status").set({
        "state_by_script": state,
        "state_by_script_date": 1
    }, merge=True)
    logging.info(f"State set by script: {state}")

def get_state_by_script(db: Client): 
    return False