# import pyrebase

# # Set the configuration for your app
# # TODO: Replace with your project's config object
# config = {
#   apiKey: "AIzaSyAi3T9eK4X9ffAGxvuy-TIbkWANdP0Ydl0",
#   authDomain: "loteriapanama-b70b9.firebaseapp.com",
#   databaseURL: "https://loteriapanama-b70b9-default-rtdb.firebaseio.com",
#   projectId: "loteriapanama-b70b9",
#   storageBucket: "loteriapanama-b70b9.appspot.com",
#   messagingSenderId: "144100090234",
#   appId: "1:144100090234:web:a6f6144cb75b80ce81b6c3",
#   measurementId: "G-ZDR3WRGV77"
# }
# firebase = pyrebase.initialize_app(config)

# # Get a reference to the database service
# db = firebase.database()

# # Try pushing some sample data
# sample = {}
# sample["Project"] = "Scrapper"
# db.child("Testing").set(sample)

#  ************************

import firebase_admin
from firebase_admin import credentials
from firebase_admin import db

cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred,{'databaseURL':'https://loteriapanama-b70b9-default-rtdb.firebaseio.com/'})

ref = db.reference('/Sorteos')
ref.push({'sorteo':'1','tipo':'Dominical','primer':'1234'})