import firebase_admin
import os
from firebase_admin import credentials
from firebase_admin import firestore

serviceAccountPath = '/usr/share/VestaStation/firebaseServiceAccount.json'

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

    def get(self, collection, conditions):
        collectionRef = self.db.collection(collection)
        for condition in conditions:
            collectionRef = collectionRef.where(condition[0], condition[1], condition[2])
        documents = list(collectionRef.get())
        print(documents)
        print('\n')
        return documents

firebase = Firebase()
