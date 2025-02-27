import logging
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


#
# SMTP Config
#
PORT = 587
SMTP_SERVER = 'smtp.gmail.com'
SENDER_EMAIL = 'faculty.electiv.courses@gmail.com'
SENDER_PASSWORD = 'vfsizenwkhheavyw'


#
#	Mail Config	
#
def send_email(subject: str, body: str, to: str) -> None:
	logging.debug("\t\t UTIL LAYER -> Mail send function")
	logging.debug(f"\t\t UTIL LAYER -> Mail Sender -> Details:\n {subject} - {body} - {to}")
	
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
		logging.debug("\t\t UTIL LAYE -> Mail Sender -> mail login...")

		srv.send_message(msg)
		logging.debug("\t\t UTIL LAYE -> Mail Sender -> sending mail...")

		srv.quit()
		logging.debug("\t\t UTIL LAYE -> Mail Sender -> quiting...")

	except Exception as e:
		pass