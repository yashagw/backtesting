from flask import Flask, request
from kiteconnect import KiteConnect
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = Flask(__name__)

# Initialize KiteConnect
API_KEY = os.getenv("KITE_API_KEY")
API_SECRET = os.getenv("KITE_API_SECRET")

kite = KiteConnect(api_key=API_KEY)

@app.route('/')
def index():
    # Generate login URL and display it
    login_url = kite.login_url()
    return f'Click here to login: <a href="{login_url}">{login_url}</a>'

@app.route('/redirect')
def redirect():
    request_token = request.args.get('request_token')
    if not request_token:
        return 'No request token found'

    try:
        # Generate session and get access token
        data = kite.generate_session(request_token, api_secret=API_SECRET)
        access_token = data["access_token"]
        
        # Save to .env file
        env_path = os.path.join(os.path.dirname(__file__), '.env')
        
        # Read existing env file content
        env_content = {}
        if os.path.exists(env_path):
            with open(env_path, 'r') as f:
                for line in f:
                    if '=' in line:
                        key, value = line.strip().split('=', 1)
                        env_content[key] = value

        # Update with new access token
        env_content['KITE_ACCESS_TOKEN'] = access_token
        
        # Write back to .env file
        with open(env_path, 'w') as f:
            for key, value in env_content.items():
                f.write(f"{key}={value}\n")
        
        return 'Access token has been saved to .env file successfully!'
    
    except Exception as e:
        return f'Error: {str(e)}'

if __name__ == '__main__':
    app.run(port=5000)
