import os
import firebase_admin
from firebase_admin import credentials, db
from dotenv import load_dotenv

# load .env file
load_dotenv()

########################
#
#   Database initialization
#
########################
def db_init():
	# Fetch db path from .env file
	db_path = os.getenv('DB_PATH')
	
	# Fetch the service account Key
	cred = credentials.Certificate(db_path)

	# Initialize the app 
	firebase_admin.initialize_app(cred, {
		'databaseURL' : 'https://smart-irrigation-system-700a6-default-rtdb.europe-west1.firebasedatabase.app'
	})
