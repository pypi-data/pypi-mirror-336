import logging
from pipefysdk.queries.query_cards import GraphQLQueries
from pipefysdk.http_client import HttpClient
from pipefysdk.mutations.mutation_cards import GraphQLMutations

class BaseService:
    """
    Base class for all services.

    url: Define the base url with the endpoint "/graphql".
    pipefy_token: Define the token to access the API without the name "Bearer".
    """
    def __init__(self, url: str, pipefy_token: str) -> None:
        self.url = url
        self._pipefy_token = pipefy_token
        self.headers = {
            'Authorization': f'Bearer {self._pipefy_token}',
            'Content-Type': 'application/json'
        }
        self.queries = GraphQLQueries()
        self.mutations = GraphQLMutations()
        self.logger = logging.getLogger(__name__)
        self.http_client = HttpClient(url, self.headers)

    def request(self, query: str) -> dict:
        """
        Make a request to the API.

        query: Define the query to be sent to the API.

        return: Return the response of the API.
        """
        self.logger.debug(f"Request headers: {self.headers}")
        self.logger.debug(f"Request query: {query}")
        return self.http_client.post(query)