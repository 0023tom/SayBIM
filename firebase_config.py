import firebase_admin
from firebase_admin import credentials, firestore
import os
import json

def initialize_firebase():
    # Priority 1: Check for Environment Variable (for Vercel/Production)
    firebase_config_env = os.environ.get('FIREBASE_CONFIG')
    if firebase_config_env:
        try:
            config_dict = json.loads(firebase_config_env)
            cred = credentials.Certificate(config_dict)
            firebase_admin.initialize_app(cred)
            print("Firebase initialized successfully via Environment Variable.")
            return firestore.client()
        except Exception as e:
            print(f"Error initializing Firebase via Env Var: {e}")

    # Priority 2: Check for local JSON file (for Local Development)
    cred_path = os.path.join(os.path.dirname(__file__), 'firebase-adminsdk.json')
    if os.path.exists(cred_path):
        try:
            cred = credentials.Certificate(cred_path)
            firebase_admin.initialize_app(cred)
            print("Firebase initialized successfully via JSON file.")
            return firestore.client()
        except Exception as e:
            print(f"Error initializing Firebase via JSON file: {e}")
    
    print("CRITICAL: No Firebase credentials found (checked Env Var and JSON file).")
    return None

# Global Firestore client
db_firestore = initialize_firebase()
