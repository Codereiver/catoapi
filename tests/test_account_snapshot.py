#
# test_account_snapshot.py - tests for the Account.accountSnapshot method
#

import unittest
import sys
import os

# Add parent directory to path to import catoapi
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from catoapi import Account


class TestAccountSnapshot(unittest.TestCase):
    #
    # Test cases for Account.accountSnapshot method
    # These tests make real API calls to Cato Networks
    #

    def setUp(self):
        #
        # Set up test fixtures before each test method
        # Requires CATO_ACCOUNT_ID and CATO_API_KEY environment variables
        #
        self.test_account_id = os.environ.get('CATO_ACCOUNT_ID')
        self.test_api_key = os.environ.get('CATO_API_KEY')

        if not self.test_account_id or not self.test_api_key:
            self.skipTest("CATO_ACCOUNT_ID and CATO_API_KEY environment variables must be set")

        self.account = Account(self.test_account_id, self.test_api_key)


    def test_account_snapshot_id_matches_account_id(self):
        #
        # Test that the id field in response matches Account.ID
        # Makes a real API call to Cato Networks
        #
        # Execute real API call
        result = self.account.accountSnapshot()

        # Verify response structure exists
        self.assertIn("id", result)
        self.assertIn("sites", result)

        # Verify the id in response matches Account.ID
        returned_id = result["id"]
        self.assertEqual(returned_id, self.account.ID)


    def test_account_snapshot_returns_valid_structure(self):
        #
        # Test that accountSnapshot returns expected data structure
        # Makes a real API call to Cato Networks
        #
        # Execute real API call
        result = self.account.accountSnapshot()

        # Verify all expected fields are present
        self.assertIn("id", result)
        self.assertIn("sites", result)
        self.assertIn("users", result)
        self.assertIn("timestamp", result)

        # Verify data types
        self.assertIsInstance(result["sites"], list)
        self.assertIsInstance(result["users"], list)
        self.assertIsInstance(result["timestamp"], str)


    def test_account_snapshot_timestamp_format(self):
        #
        # Test that accountSnapshot returns properly formatted timestamp
        # Makes a real API call to Cato Networks
        #
        # Execute real API call
        result = self.account.accountSnapshot()

        timestamp = result["timestamp"]

        # Verify timestamp is not empty
        self.assertIsNotNone(timestamp)
        self.assertTrue(len(timestamp) > 0)

        # Timestamp should be a string (ISO format expected)
        self.assertIsInstance(timestamp, str)






if __name__ == '__main__':
    unittest.main()
