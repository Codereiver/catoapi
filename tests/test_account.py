#
# test_account.py - tests for the Account class
#

import unittest
import sys
import os

# Add parent directory to path to import catoapi
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from catoapi import Account


class TestAccountInitialization(unittest.TestCase):
    #
    # Test cases for Account class initialization
    #

    def setUp(self):
        #
        # Set up test fixtures before each test method
        # Load account ID and API key from environment variables
        #
        self.test_account_id = os.environ.get('CATO_ACCOUNT_ID', '12345')
        self.test_api_key = os.environ.get('CATO_API_KEY', 'test_api_key_default')


    def test_account_init_with_valid_params(self):
        #
        # Test that Account initializes correctly with valid ID and api_key
        #
        account = Account(self.test_account_id, self.test_api_key)

        self.assertEqual(account.ID, self.test_account_id)
        self.assertEqual(account.api_key, self.test_api_key)


    def test_account_init_with_numeric_id(self):
        #
        # Test that Account works with numeric ID
        #
        account_id = 67890
        api_key = "another_api_key_xyz789"
        account = Account(account_id, api_key)
        self.assertEqual(account.ID, account_id)
        self.assertEqual(account.api_key, api_key)


    def test_account_init_stores_id_privately(self):
        #
        # Test that ID is stored in private attribute _ID
        #
        account = Account(self.test_account_id, self.test_api_key)

        self.assertTrue(hasattr(account, '_ID'))
        self.assertEqual(account._ID, self.test_account_id)


    def test_account_init_stores_api_key_privately(self):
        #
        # Test that api_key is stored in private attribute _api_key
        #
        account = Account(self.test_account_id, self.test_api_key)

        self.assertTrue(hasattr(account, '_api_key'))
        self.assertEqual(account._api_key, self.test_api_key)


    def test_account_init_with_default_url(self):
        #
        # Test that Account uses default URL when not specified
        #
        account = Account(self.test_account_id, self.test_api_key)

        expected_url = "https://api.catonetworks.com/api/v1/graphql2"
        self.assertEqual(account._url, expected_url)


    def test_account_init_with_custom_url(self):
        #
        # Test that Account accepts custom URL parameter
        #
        custom_url = "https://custom.api.example.com"
        account = Account(self.test_account_id, self.test_api_key, url=custom_url)

        self.assertEqual(account._url, custom_url)


    def test_account_init_stores_url_privately(self):
        #
        # Test that URL is stored in private attribute _url
        #
        custom_url = "https://test.catonetworks.com"
        account = Account(self.test_account_id, self.test_api_key, url=custom_url)

        self.assertTrue(hasattr(account, '_url'))
        self.assertEqual(account._url, custom_url)


if __name__ == '__main__':
    unittest.main()