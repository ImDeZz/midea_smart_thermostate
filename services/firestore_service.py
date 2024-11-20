import firebase_admin
from firebase_admin import credentials, firestore
from google.cloud.firestore_v1 import Client

# Path to your service account key JSON file
service_account_path = "secrets/midea_smart_thermostate_service_account.json"

# Initialize the Firebase app
def get_firestore() :
    cred = credentials.Certificate(service_account_path)
    firebase_admin.initialize_app(cred)

    # Access Firestore
    db = firestore.client()

    print("Firebase connection initialized successfully.")
    return db

def get_thresholds(db: Client):
    doc = db.collection("thresholds").document("thresholds").get()
    target_temperature = doc.get("target_temperature")
    turn_on_threhold = doc.get("turn_on_threhold")

    print(f"Target temp: {target_temperature}")
    print(f"Turn on temp: {turn_on_threhold}")
    
    return target_temperature, turn_on_threhold