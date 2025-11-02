#
# test_account_send.py - tests for the Account.send method
#

import unittest
import sys
import os
import json
import gzip
from unittest.mock import Mock, patch, MagicMock

# Add parent directory to path to import catoapi
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from catoapi import Account


class TestAccountSend(unittest.TestCase):
    #
    # Test cases for Account.send method
    #

    def setUp(self):
        #
        # Set up test fixtures before each test method
        #
        self.test_account_id = os.environ.get('CATO_ACCOUNT_ID', '12345')
        self.test_api_key = os.environ.get('CATO_API_KEY', 'test_api_key_default')
        self.account = Account(self.test_account_id, self.test_api_key)

        # Note: Account needs a _url attribute for send() to work
        # This should be set in __init__ or as a parameter
        self.test_url = "https://api.catonetworks.com/api/v1/graphql2"
        self.account._url = self.test_url


    @patch('urllib.request.urlopen')
    def test_send_successful_request(self, mock_urlopen):
        #
        # Test successful GraphQL request
        #
        # Mock response data
        response_data = {"data": {"result": "success"}}
        response_json = json.dumps(response_data)
        response_compressed = gzip.compress(response_json.encode('utf-8'))

        # Create mock response object
        mock_response = Mock()
        mock_response.read.return_value = response_compressed
        mock_urlopen.return_value = mock_response

        # Test data
        operation = "TestOperation"
        query = "query TestOperation { test }"
        variables = {"var1": "value1"}

        # Execute
        result = self.account.send(operation, variables, query)

        # Verify
        self.assertEqual(result, response_data)
        mock_urlopen.assert_called_once()


    @patch('urllib.request.urlopen')
    def test_send_creates_correct_request(self, mock_urlopen):
        #
        # Test that send creates request with correct headers and body
        #
        # Mock response
        response_data = {"data": {"test": "data"}}
        response_json = json.dumps(response_data)
        response_compressed = gzip.compress(response_json.encode('utf-8'))
        mock_response = Mock()
        mock_response.read.return_value = response_compressed
        mock_urlopen.return_value = mock_response

        # Test data
        operation = "GetUsers"
        query = "query GetUsers { users { id name } }"
        variables = {"limit": 10}

        # Execute
        result = self.account.send(operation, variables, query)

        # Get the Request object that was passed to urlopen
        call_args = mock_urlopen.call_args
        request_obj = call_args[0][0]

        # Verify request properties
        self.assertEqual(request_obj.full_url, self.test_url)
        self.assertEqual(request_obj.headers.get('Content-type'), 'application/json')
        self.assertEqual(request_obj.headers.get('X-api-key'), self.test_api_key)
        self.assertEqual(request_obj.headers.get('Accept-encoding'), 'gzip, deflate, br')

        # Verify request body
        expected_body = json.dumps({
            "operationName": operation,
            "query": query,
            "variables": variables
        })
        self.assertEqual(request_obj.data.decode('ascii'), expected_body)


    @patch('urllib.request.urlopen')
    def test_send_with_empty_variables(self, mock_urlopen):
        #
        # Test send with empty variables dict
        #
        response_data = {"data": {"result": "ok"}}
        response_json = json.dumps(response_data)
        response_compressed = gzip.compress(response_json.encode('utf-8'))
        mock_response = Mock()
        mock_response.read.return_value = response_compressed
        mock_urlopen.return_value = mock_response

        operation = "SimpleQuery"
        query = "query SimpleQuery { status }"
        variables = {}

        result = self.account.send(operation, variables, query)

        self.assertEqual(result, response_data)


    @patch('urllib.request.urlopen')
    def test_send_handles_utf8_response(self, mock_urlopen):
        #
        # Test that send correctly decodes UTF-8 responses
        #
        response_data = {"data": {"message": "Hello 世界 🌍"}}
        response_json = json.dumps(response_data, ensure_ascii=False)
        response_compressed = gzip.compress(response_json.encode('utf-8'))
        mock_response = Mock()
        mock_response.read.return_value = response_compressed
        mock_urlopen.return_value = mock_response

        operation = "TestUTF8"
        query = "query TestUTF8 { message }"
        variables = {}

        result = self.account.send(operation, variables, query)

        self.assertEqual(result["data"]["message"], "Hello 世界 🌍")


    @patch('urllib.request.urlopen')
    def test_send_timeout_parameter(self, mock_urlopen):
        #
        # Test that send passes timeout parameter to urlopen
        #
        response_data = {"data": {}}
        response_json = json.dumps(response_data)
        response_compressed = gzip.compress(response_json.encode('utf-8'))
        mock_response = Mock()
        mock_response.read.return_value = response_compressed
        mock_urlopen.return_value = mock_response

        operation = "TestOp"
        query = "query TestOp { test }"
        variables = {}

        result = self.account.send(operation, variables, query)

        # Verify timeout was passed
        call_kwargs = mock_urlopen.call_args[1]
        self.assertEqual(call_kwargs.get('timeout'), 10)


if __name__ == '__main__':
    unittest.main()
