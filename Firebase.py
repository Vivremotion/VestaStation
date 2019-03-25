import firebase_admin
import os
from firebase_admin import credentials
from firebase_admin import firestore

serviceAccountPath = '/usr/share/Station/firebaseServiceAccount.json'

class Firebase:
    db = {}

    def initialize(self):
        os.environ["GOOGLE_APPLICATION_CREDENTIALS"]=serviceAccountPath
        cred = credentials.Certificate(serviceAccountPath)
        firebase_admin.initialize_app(cred)
        self.db = firestore.Client()

    def send(self, collection, id, value):
        document = self.db.collection(collection).document(id)
        document.set(value)
        return document

firebase = Firebase()
