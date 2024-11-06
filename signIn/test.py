import pytest
from signIn.signIn import app
from unittest.mock import Mock
import os

# Enable insecure transport for OAuth (only for testing purposes)
os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'

@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client

def test_callback_rejects_non_aucegypt_email(client, mocker):
    # Mock the ID token verification to simulate a non-AUC email
    mocker.patch("google.oauth2.id_token.verify_oauth2_token", return_value={"email": "user@nonauc.edu"})
    # Mock fetch_token to bypass the actual token exchange
    mocker.patch("google_auth_oauthlib.flow.Flow.fetch_token", return_value=None)

    # Mock credentials to include _id_token attribute
    mocked_credentials = Mock()
    mocked_credentials._id_token = "mocked_id_token"
    mocker.patch("google_auth_oauthlib.flow.Flow.credentials", new_callable=mocker.PropertyMock, return_value=mocked_credentials)

    with client.session_transaction() as session:
        session["state"] = "state"

    # Simulate callback endpoint call with a mocked authorization code
    response = client.get("/callback?state=state&code=auth_code")
    
    # Validate the response is an error due to non-AUC email
    assert response.json["status"] == "error", "Expected an error status for non-AUC email"
    assert "Access restricted to @aucegypt.edu emails only" in response.json["message"]

def test_callback_allows_aucegypt_email(client, mocker):
    # Mock the ID token verification to simulate a valid AUC email
    mocker.patch("google.oauth2.id_token.verify_oauth2_token", return_value={"email": "mhebishy@aucegypt.edu"})
    # Mock fetch_token to bypass the actual token exchange
    mocker.patch("google_auth_oauthlib.flow.Flow.fetch_token", return_value=None)

    # Mock credentials to include _id_token attribute
    mocked_credentials = Mock()
    mocked_credentials._id_token = "mocked_id_token"
    mocker.patch("google_auth_oauthlib.flow.Flow.credentials", new_callable=mocker.PropertyMock, return_value=mocked_credentials)

    # Mock database connection and query for user existence check
    mocker.patch("signIn.signIn.mysql.connector.connect")
    mock_conn = mocker.patch("signIn.signIn.mysql.connector.connect")
    mock_cursor = mock_conn.return_value.cursor.return_value
    mock_cursor.fetchone.return_value = None  # Simulate user does not exist
    
    with client.session_transaction() as session:
        session["state"] = "state"

    # Simulate callback endpoint call with a mocked authorization code
    response = client.get("/callback?state=state&code=auth_code")
    
    # Validate the response is success for valid AUC email
    assert response.json["status"] == "success", "Expected a success status for AUC email"
    assert ("User signed in successfully" in response.json["message"] or 
            "User registered successfully" in response.json["message"]), "Expected sign-in or registration success message"
