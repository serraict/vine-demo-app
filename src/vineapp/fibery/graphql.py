"""Fibery GraphQL client.

Example usage:

    try:
        client = get_fibery_client()
        # Query to get schema information
        query = '''
            query {
                __schema {
                    types {
                        name
                        fields {
                            name
                        }
                    }
                }
            }
        '''
        result = client.execute(query)
        types = [t for t in result['data']['__schema']['types'] 
                if t['name'].startswith('Public') and t['fields']]
        for type_info in types:
            print(f"Found type: {type_info['name']}")
            
    except ValueError as e:
        print(f"Configuration error: {e}")
    except requests.RequestException as e:
        print(f"API request failed: {e}")
"""

import os
from dataclasses import dataclass
import requests


@dataclass
class FiberyGraphQLClient:
    """Client for interacting with Fibery's GraphQL API."""

    url: str
    token: str

    def execute(self, query: str) -> dict:
        """Execute a GraphQL query against the Fibery API.

        Args:
            query: The GraphQL query to execute

        Returns:
            The JSON response from the API

        Raises:
            requests.RequestException: If the request fails or returns an error status
        """
        headers = {
            "Authorization": f"Token {self.token}",
            "Content-Type": "application/json",
        }

        response = requests.post(self.url, headers=headers, json={"query": query})
        response.raise_for_status()  # Raise exception for error status codes

        return response.json()


def get_fibery_client() -> FiberyGraphQLClient:
    """Get a configured Fibery GraphQL client using environment variables.

    Returns:
        A configured FiberyGraphQLClient instance

    Raises:
        ValueError: If required environment variables are not set
    """
    token = os.getenv("VINEAPP_FIBERY_TOKEN")
    if not token:
        raise ValueError("VINEAPP_FIBERY_TOKEN environment variable is not set")

    from vineapp.fibery.models import get_fibery_info

    info = get_fibery_info()

    return FiberyGraphQLClient(url=str(info.graphql_url), token=token)
