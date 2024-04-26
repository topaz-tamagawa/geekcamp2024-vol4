import os
import base64

import firebase_admin
import json

def init_firebase_app():
    if "FIREBASE_SERVICE_ACCOUNT_CREDENTIALS" in os.environ :
        credentials_base64 = os.environ["FIREBASE_SERVICE_ACCOUNT_CREDENTIALS"]
        credentials_json = json.loads(base64.b64decode(credentials_base64).decode("utf-8"))
        certificate = firebase_admin.credentials.Certificate(credentials_json)
        app = firebase_admin.initialize_app(certificate)
    else:
        app = firebase_admin.initialize_app()

    return app
