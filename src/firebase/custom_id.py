import logging
from firebase_admin import credentials, db

#####################
#
#	Auto-increment function for firebase IDs
#
#####################
def id_incrementation(type):
    # Reference to the current ID
    id_ref = db.reference(f'irrigation-system/{type}_current_id')
    current_id = id_ref.get()  

    logging.info(f"Fetched last db sensors ID: {current_id}")

    # Initialize ID if it doesn't exist
    if current_id is None:
        current_id = 1  
    else:
        current_id += 1 

    # Update the current ID in the database
    id_ref.set(current_id)

    return current_id