#
# catoapi.py - wrapper for the Cato Networks GraphQL API
#

import gzip
import json
import ssl
import urllib.request

class Account:

    def __init__(self, ID, api_key, url="https://api.catonetworks.com/api/v1/graphql2"):
        #
        # ID:       The CMA account ID
        # api_key:  API key to use with this connection
        #
        self._ID = ID
        self._api_key = api_key
        self._url = url


    @property
    def ID(self):
        return self._ID
    

    @property
    def api_key(self):
        return self._api_key
    

    ################################################################################
    ################################################################################
    ################################################################################
    #
    # Engine functions
    #

    def send(self, operation, variables, query):
        #
        # Send an API request and return the response as a Python object.
        #
        # Returns the Python object converted from JSON response.
        # Raises CatoNetworkError for connection issues.
        # Raises CatoGraphQLError if the API returns errors.
		#
        body = json.dumps({"operationName": operation, "query":query, "variables":variables})
        body = body.encode("ascii")
        headers = {
            "Content-Type": "application/json",
            "Accept-Encoding": "gzip, deflate, br",
            "X-api-key": self._api_key
        }
        request = urllib.request.Request(url=self._url, data=body, headers=headers)
        response = urllib.request.urlopen(request, timeout=10)
        response_data = gzip.decompress(response.read())
        response_text = response_data.decode('utf-8','replace')
        response_obj = json.loads(response_text)
        if "errors" in response_obj:
            raise CatoAPIError(response_text)
        return response_obj


    class CatoAPIError(Exception):
        """Base exception for Cato API errors"""
        pass


    ################################################################################
    ################################################################################
    ################################################################################
    #
    # API calls
    #

    def accountSnapshot(self):
        #
        # accountSnapshot call
        #
        variables = {
            "accountID": self.ID
        }
        query = """
query accountSnapshot($accountID:ID!) {
  accountSnapshot(accountID:$accountID) {
    id
    sites {
      connectivityStatus
      haStatus{
        readiness
        wanConnectivity
        keepalive
        socketVersion
      }
      operationalStatus
      lastConnected
      connectedSince
      devices {
        connected
        version
      }
    }
    users {
      connectivityStatus
      connectedInOffice
      name
      deviceName
    }
    timestamp
  }
}"""
        return self.send("accountSnapshot", variables, query)["data"]["accountSnapshot"]