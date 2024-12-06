from flask import Flask, redirect, url_for, session, render_template
from authlib.integrations.flask_client import OAuth
from dotenv import load_dotenv
import os
import ssl

# Load environment variables from .env file
load_dotenv()

# App configuration
app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY')  # Use the secret key from the .env file


# OAuth configuration
oauth = OAuth(app)
google = oauth.register(
    name='google',
    client_id=os.getenv('GOOGLE_ID'),
    client_secret=os.getenv('GOOGLE_SECRET'),
    server_metadata_url='https://accounts.google.com/.well-known/openid-configuration',
    client_kwargs={'scope': 'openid email profile'},
)

# Routes
@app.route('/')
def index():
    return render_template('index.html')  # Minimal landing page with sign-in button

@app.route('/login')
def login():
    return google.authorize_redirect(url_for('auth', _external=True))

@app.route('/auth')
def auth():
    try:
        # Fetch the token
        token = google.authorize_access_token()
        
        # Use the token to fetch user info
        user_info = google.get('https://www.googleapis.com/oauth2/v2/userinfo').json()

        # Store user info in session
        session['user'] = user_info

        # Redirect to the profile page
        return redirect(url_for('profile'))

    except Exception as e:
        # Log the error and return a helpful message
        print(f"Error during authentication: {e}")
        return "An error occurred during authentication", 500


@app.route('/profile')
def profile():
    user = session.get('user')
    if not user:
        return redirect(url_for('index'))
    return render_template('profile.html', user=user)

@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('index'))

if __name__ == '__main__':
    # Run Flask with SSL (certificate and key files)
    context=ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
    context.load_cert_chain('crt.crt', 'key.key')
    app.run(ssl_context=context, host='127.0.3.3', port=5000)