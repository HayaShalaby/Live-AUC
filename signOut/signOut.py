from flask import Flask, jsonify, session
import os 

app = Flask(__name__)
app.secret_key = os.urandom(24)

# Sign-out function
@app.route("/signout", methods=["POST"])
def signout():
    try:
        # Clear the session data
        session.clear()
        return jsonify({"status": "success", "message": "Successfully signed out"}), 200
    except Exception as e:
        print("Error during sign-out:", e)
        return jsonify({"status": "error", "message": "An error occurred during sign-out"}), 500

if __name__ == "__main__":
    app.run(debug=True)
