import unittest
from signOut import app  

class SignOutTestCase(unittest.TestCase):
    def setUp(self):
        # Set up the test client
        self.app = app.test_client()
        self.app.testing = True

    def test_signout_successful(self):
        # First, we simulate signing in by setting session data
        with self.app.session_transaction() as session:
            session['user'] = {'email': 'testuser@aucegypt.edu', 'name': 'Test User'}

        # Send POST request to /signout
        response = self.app.post('/signout')

        # Parse the JSON response
        response_json = response.get_json()

        # Check that the response status is success
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response_json['status'], 'success')
        self.assertEqual(response_json['message'], 'Successfully signed out')

        # Check that the session is cleared
        with self.app.session_transaction() as session:
            self.assertNotIn('user', session)

    def test_signout_without_session(self):
        # Send POST request to /signout without a logged-in session
        response = self.app.post('/signout')
        response_json = response.get_json()

        # Check that the response is still successful even if no session exists
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response_json['status'], 'success')
        self.assertEqual(response_json['message'], 'Successfully signed out')

if __name__ == "__main__":
    unittest.main()
