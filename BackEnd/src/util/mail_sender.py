import logging
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from src.classes.FieldDTO import FieldDTO


#
# SMTP Config
#
PORT = 587
SMTP_SERVER = 'smtp.gmail.com'
SENDER_EMAIL = 'faculty.electiv.courses@gmail.com'
SENDER_PASSWORD = 'vfsizenwkhheavyw'


#
#	Mail Defines
#
def generate_field_creation_email_body(mail: str, location: str, field_dto: FieldDTO) -> str:
	email_body = f"""
		Dear {mail},

		We're pleased to inform you that your new field has been successfully registered in our system!

		Field Details:
		📍 Location: {location}
		🌱 Crop: {field_dto.crop_name}
		📏 Dimensions: {field_dto.length}m × {field_dto.width}m
		🌍 Soil Type: {field_dto.soil_type}

		You can now monitor this field through your dashboard. The following sensors have been assigned to this field:
		{field_dto.sensors}

		Thank you for using our agricultural management system.

		Happy farming!

		Best regards,
		Team
	"""

	return email_body

def generate_field_update_mail_body(mail: str, location: str, field_dto: FieldDTO) -> str:
	body = f"""
		Dear {mail},

		Your field details have been successfully updated:

		🌾 **New Field Details**  
		📍 Location: {location}  
		🌱 Crop: {field_dto.crop_name}  
		📏 Dimensions: {field_dto.length}m × {field_dto.width}m
		⛰️ Slope: {field_dto.slope}°  
		🌱 Soil Type: {field_dto.soil_type}

		You can view the updated data in your dashboard. If these changes were unexpected, please contact our support team immediately.

		Happy monitoring!  

		Best regards,  
		Team
	"""
	return body

def generate_field_delete_mail_body(mail: str, location: str, crop_name: str) -> str:
	body = f"""
		Dear {mail},

		We confirm your field has been permanently deleted from our system:

		🗑️ **Deleted Field Details**  
		📍 Location: {location}  
		🌱 Crop: {crop_name}  

		All associated data has been removed from our records. If this was done in error, please contact our support team immediately.

		Best regards,  
		Team
	"""
	return body

#
#	Mail Config	
#
def send_email(subject: str, body: str, to: str) -> None:
	# Create the email message
	msg = MIMEMultipart()
	msg['Subject'] = subject
	msg['From'] = SENDER_EMAIL
	msg['To'] = to
	msg.attach(MIMEText(body, 'plain'))

	try:
		# Set up the SMTP server and send the email
		srv = smtplib.SMTP(SMTP_SERVER, PORT)
		srv.starttls() 
		srv.login(SENDER_EMAIL, SENDER_PASSWORD) 
		srv.send_message(msg)
		srv.quit()

	except Exception as e:
		pass