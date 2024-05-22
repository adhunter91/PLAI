import unittest
from flask import json
from app import create_app  # Adjust the import according to your project structure


class TestWebhook(unittest.TestCase):
    def setUp(self):
        """Set up a test client for the Flask application."""
        self.app = create_app('test_config.py')
        self.app.config['TESTING'] = True
        self.client = self.app.test_client()

    def test_webhook_event(self):
        """Test the webhook endpoint with a simulated POST request."""
        # Example payload that the webhook might receive
        payload = {'name': 'Test Event', 'data': 'Some data'}

        # Send a POST request to the webhook endpoint with JSON data
        response = self.client.post('/webhook/event', data=json.dumps(payload), content_type='application/json')

        # Check that the response is 200 OK
        self.assertEqual(response.status_code, 200)

        # Check the response data
        response_data = json.loads(response.data)
        self.assertEqual(response_data['status'], 'success')
        self.assertEqual(response_data['data_received'], payload)


if __name__ == '__main__':
    unittest.main()