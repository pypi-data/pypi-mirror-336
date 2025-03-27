from katapult_api.katapult import Katapult
from typing import Any, Dict


class KatapultNice(Katapult):
    """Used to access and parse Katapult data through the Katapult API

    This class is used to house methods used to make requests to the Katapult API. Root attributes are used in the
    creation of a root url and any parameters required for all requests. Response are parsed into an easy-to-use format.

    Attributes:
        _base_url: A string used as the root url for requests.
        root_parms: A dictionary of parameters that are always required for any request (e.g. api_key).
    """

    def __init__(
            self,
            api_key: str,
            servername: str = "techserv",
            concurrent_rate_limit: int = 99,
    ):
        super().__init__(api_key, servername, concurrent_rate_limit)

    async def job_nodes(self, job_id: str) -> Dict[str, Any]:
        """Fetches a single job's nodes"""
        response = await super().job(job_id)
        job_data = response.json()

        nodes = job_data.get("nodes", {})
        cleaned_dict = {}

        for key, value in nodes.items():
            node_dict = {
                "latitude": value.get("latitude"),
                "longitude": value.get("longitude"),
                "attributes_raw": value.get("attributes", {}),
                "attributes": self.clean_attributes(value.get("attributes", {})),
            }
            cleaned_dict[key] = node_dict

        return cleaned_dict

    def clean_attributes(self, attributes: dict) -> dict:
        """Removes unnecessary intermediate keys when there is only one nested key."""
        if not isinstance(attributes, dict):
            return attributes

        cleaned = {}
        for key, value in attributes.items():
            if isinstance(value, dict) and len(value) == 1:
                inner_key, inner_value = next(iter(value.items()))
                cleaned[key] = inner_value
            elif isinstance(value, dict):
                cleaned[key] = self.clean_attributes(value)
            else:
                cleaned[key] = value

        return cleaned
