import requests
import base64
from typing import Any, Dict, Optional, Iterable

from singer_sdk.streams import RESTStream
from singer_sdk.authenticators import APIAuthenticatorBase, SimpleAuthenticator
from singer_sdk import (
    Property,
    PropertiesList,
    StringType,
)

class TapSoccerStream(RESTStream):
    """Soccer stream class."""
    @property
    def url_base(self) -> str: 
      return f"http://api.football-data.org/v2/2000"

    def get_url_params(self, partition: Optional[dict]) -> Dict[str, Any]:
        """Return a dictionary of values to be used in URL parameterization."""
        params = {}
        starting_datetime = self.get_starting_datetime(partition)
        if starting_datetime:
            params.update({"updated": starting_datetime})
        return params

    @property
    def authenticator(self) -> APIAuthenticatorBase:
        http_headers = {}
        auth_token = self.config.get("auth_token")
        basic_auth = f"{auth_token}:nothingtoseehere"
        http_headers["Authorization"] = "Basic " + base64.b64encode(basic_auth.encode("utf-8")).decode('utf-8')
        http_headers["Content-Type"] = "application/json"
        http_headers["Accept"] = "application/json"
        if self.config.get("user_agent"):
            http_headers["User-Agent"] = self.config.get("user_agent")
        return SimpleAuthenticator(stream=self, http_headers=http_headers)

    def parse_response(self, response: requests.Response) -> Iterable[dict]:
        """Parse the response and return an iterator of result rows."""
        resp_json = response.json()
        for row in resp_json.get("name"):
            yield row

class Teams(TapSoccerStream):
    name = "teams"
    path = "/teams"
    primary_keys = ["id"]
    replication_key = None
    schema = PropertiesList(
              Property("id", StringType),
              Property("name", StringType),

    ).to_dict()