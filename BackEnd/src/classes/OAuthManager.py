from authlib.integrations.flask_client import OAuth

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
			client_id='445623818086-r55c913j7s5ij4cmu52meamluj7q1u4t.apps.googleusercontent.com',
			client_secret='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',
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