from typing import List
from singer_sdk import Tap, Stream
from singer_sdk import (

    PropertiesList,
    StringType,
)

from tap_soccer.streams import (
    Teams,
)

PLUGIN_NAME = "tap-soccer"

STREAM_TYPES = [
  Teams,
]

class TapSoccer(Tap):
    """Soccer tap class."""

    name = "tap-soccer"
    config_jsonschema = PropertiesList(
        StringType("auth_token", required=True),
    ).to_dict()

    def discover_streams(self) -> List[Stream]:
        """Return a list of discovered streams."""
        return [stream_class(tap=self) for stream_class in STREAM_TYPES]

cli = TapSoccer.cli