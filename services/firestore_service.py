import logging
import firebase_admin
from firebase_admin import credentials, firestore
from google.cloud.firestore_v1 import Client
import os

# Get the directory where the script is located
script_dir = os.path.dirname(os.path.realpath(__file__))

# Build the path to the secrets folder
service_account_path = os.path.join(script_dir, "..", "secrets", "midea_smart_thermostate_service_account.json")

# Optionally, print to verify the correct path
logging.info(f"Service account path: {service_account_path}")

# Initialize the Firebase app
def get_firestore() :
    print(service_account_path)
    cred = credentials.Certificate(service_account_path)
    print(f"{cred}")
    firebase_admin.initialize_app(cred)

    # Access Firestore
    db = firestore.client()
    
    logging.info("Firebase connection initialized successfully.")
    return db

def get_thresholds(db: Client):
    doc = db.collection("thresholds").document("thresholds").get()
    target_temperature = doc.get("target_temperature")
    turn_on_threhold = doc.get("turn_on_threhold")

    logging.info(f"Target temp: {target_temperature}")
    logging.info(f"Turn on temp: {turn_on_threhold}")
    
    return target_temperature, turn_on_threhold