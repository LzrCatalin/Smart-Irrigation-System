import os
from authlib.integrations.flask_client import OAuth
from dotenv import load_dotenv

# load .env file
load_dotenv()
GOOGLE_CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID")
GOOGLE_CLIENT_SECRET = os.getenv("GOOGLE_CLIENT_SECRET")


#######################
#
# OAuth 2.0 Config - GOOGLE
#
#######################
class OAuthManager:

	def __init__(self, app=None):
		self.oauth = OAuth()
		if app:
			self.init_app(app)

	def init_app(self, app):
		self.oauth.init_app(app)
		self.oauth.register(
			name='google',
			client_id=GOOGLE_CLIENT_ID,
			client_secret=GOOGLE_CLIENT_SECRET,
			access_token_url='https://accounts.google.com/o/oauth2/token',
			access_token_params=None,
			authorize_url='https://accounts.google.com/o/oauth2/auth',
			authorize_params=None,
			api_base_url='https://www.googleapis.com/oauth2/v1/',
			userinfo_endpoint='https://openidconnect.googleapis.com/v1/userinfo',
			client_kwargs={'scope': 'email profile'},
			server_metadata_url='https://accounts.google.com/.well-known/openid-configuration'
		)

	def get_provider(self, name):
		return self.oauth.create_client(name)