import firebase_admin
from firebase_admin import credentials, db

########################
#
#   Database initialization
#
########################
def db_init():
	# Fetch the service account Key
	cred = credentials.Certificate('/home/catalin/Documents/smart-irrigation-system-700a6-firebase-adminsdk-2uobl-aff09eb01c.json')

	# Initialize the app 
	firebase_admin.initialize_app(cred, {
		'databaseURL' : 'https://smart-irrigation-system-700a6-default-rtdb.europe-west1.firebasedatabase.app'
	})
