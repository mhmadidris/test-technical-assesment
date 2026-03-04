import firebase_admin
from firebase_admin import credentials
from .env import env 
import json
import os

def init_firebase():
    if not os.path.exists("firebase.json"):
        print("Warning: firebase.json not found. Skipping Firebase initialization.")
        return

    try:
        with open("firebase.json", "r") as f:
            fb_data = json.load(f)
            if fb_data.get("type") != "service_account" or fb_data.get("project_id") == "PROJECT_ID":
                print("Warning: firebase.json is a placeholder or invalid. Skipping Firebase initialization.")
                return
    except Exception as e:
        print(f"Warning: Failed to read firebase.json: {e}. Skipping Firebase initialization.")
        return

    # Due to this method called on the main.py
    # it has same directory level with firebase.json file
    cred = credentials.Certificate("firebase.json")
    config = {
        'storageBucket': env.FIREBASE_STORAGE_BUCKET_URL
    }
    firebase_admin.initialize_app(cred, config)