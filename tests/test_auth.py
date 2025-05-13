import unittest
import sys
import os
import json
sys.path.append(os.path.abspath(os.path.dirname(__file__) + '/..'))  # Go up one level from tests/

from app import app  # Now imports from backend/app.py

class TestAuth(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()

    def test_login(self):
        response = self.app.post('/api/auth/login', json={
        'email': 'test_Souha@example.com',
        'password': 'hashed_password_here'
        })
        
        # Print response data for debugging
        print("Response Status Code:", response.status_code)
        print("Response Data:", response.data.decode('utf-8'))
        
        self.assertEqual(response.status_code, 200)

if __name__ == '__main__':
    unittest.main()