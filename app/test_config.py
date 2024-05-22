# Configuration specific to testing
TESTING = True
SERVER_NAME = 'localhost:5000'  # Specify server name to enable url_for() without request context
SECRET_KEY = 'verysecrettestkey'  # Required if you are using sessions or CSRF protection