from flask import Flask, redirect, request, jsonify, url_for, session
from flask_cors import CORS
from google_auth_oauthlib.flow import Flow
from google.oauth2 import id_token
from google.auth.transport import requests
import os
from dotenv import load_dotenv
import mysql.connector

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv("FLASK_SECRET_KEY", os.urandom(24))
CORS(app)

# Enable insecure transport for local testing (HTTP instead of HTTPS)
os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'

# Google OAuth client configuration as a dictionary
client_config = {
    "web": {
        "client_id": os.getenv("GOOGLE_CLIENT_ID"),
        "project_id": os.getenv("GOOGLE_PROJECT_ID"),
        "auth_uri": os.getenv("GOOGLE_AUTH_URI"),
        "token_uri": os.getenv("GOOGLE_TOKEN_URI"),
        "auth_provider_x509_cert_url": os.getenv("GOOGLE_AUTH_PROVIDER_CERT_URL"),
        "client_secret": os.getenv("GOOGLE_CLIENT_SECRET"),
        "redirect_uris": [os.getenv("REDIRECT_URI", "http://127.0.0.1:5000/callback")]
    }
}

# Step 1: Redirect user to Google for authentication
@app.route("/login", methods=["GET"])
def login():
    flow = Flow.from_client_config(
        client_config,
        scopes=[
            "openid",
            "https://www.googleapis.com/auth/userinfo.email",
            "https://www.googleapis.com/auth/userinfo.profile"
        ],
        redirect_uri=url_for("callback", _external=True)
    )
    auth_url, _ = flow.authorization_url(prompt="consent")
    return jsonify({"auth_url": auth_url})

# Step 2: Google redirects back to this route with an authorization code
@app.route("/callback", methods=["GET"])
def callback():
    try:
        flow = Flow.from_client_config(
            client_config,
             scopes=[
                "openid",
                "https://www.googleapis.com/auth/userinfo.email",
                "https://www.googleapis.com/auth/userinfo.profile"
],
            redirect_uri=url_for("callback", _external=True)
        )
        flow.fetch_token(authorization_response=request.url)

        credentials = flow.credentials
        id_info = id_token.verify_oauth2_token(
            credentials._id_token, requests.Request(), client_config["web"]["client_id"]
        )

        email = id_info.get("email")
        name = id_info.get("name")

        if not email.endswith("@aucegypt.edu"):
            return jsonify({"status": "error", "message": "Access restricted to @aucegypt.edu emails only"}), 403

        # Return success message with user info (database operations can be added here)
        return jsonify({"status": "success", "message": "Authentication successful", "user": {"email": email, "name": name}})

    except Exception as e:
        print("Error in callback:", e)
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route("/", methods=["GET"])
def home():
    return "Welcome to the Live-AUC Sign-In API"

if __name__ == "__main__":
    app.run(debug=True)
