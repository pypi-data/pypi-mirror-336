# TODO do we want the methods named get_**, post_**, del_** etc

from typing import Literal, Optional, Union
from urllib.parse import urljoin

from .client import Client, Response
from .enums import RequestEnums


class Katapult(Client):
    _CONCURRENT_RATE_LIMT = 99
    _BASE_URL = "https://{}.katapultpro.com/api/"

    def __init__(
        self,
        api_key: str,
        servername: str = "techserv",
        concurrent_rate_limit: int = 99,
    ):
        super().__init__(
            self._BASE_URL.format(servername), api_key, concurrent_rate_limit
        )

    async def job_lists(
        self, order_by_child: Optional[str] = None, equal_to: Optional[str] = None
    ) -> Response:
        return await self.request(
            "GET",
            self._build_url("jobs"),
            params={"orderByChild": order_by_child, "equalTo": equal_to},
        )

    async def job(self, job_id: str) -> Response:
        return await self.request(
            RequestEnums.GET.value, self._build_url(f"jobs/{job_id}")
        )

    async def jobs_in_folder(self, folder_path: Union[str, None] = None) -> Response:
        return await self.request(
            RequestEnums.GET.value,
            self._build_url("folders"),
            params={"folderPath": folder_path},
        )

    async def get_model_list(self) -> Response:
        return await self.request(RequestEnums.GET.value, self._build_url("models"))

    async def get_photo(
        self,
        job_id: str,
        photo_id: str,
        download_file: bool = False,
        file_size: Optional[
            Literal["full", "extra_large", "large", "small", "tiny"]
        ] = "full",
    ) -> Response:
        if file_size not in ["full", "extra_large", "large", "small", "tiny"]:
            raise ValueError(
                "file_size is incorrect, must be one of the following: full, extra_large, large, small, tiny"
            )

        params = {"download_file": download_file, "file_size": file_size}

        return await self.request(
            RequestEnums.GET.value,
            self._build_url(f"jobs/{job_id}/photos/{photo_id}"),
            params=params,
        )

    async def create_job(
        self,
        name: str,
        model: str,
        job_project_folder_path: Optional[str] = None,
        **kwargs,
    ) -> Response:
        body = {
            "name": name,
            "model": model,
            "jobProjectFolderPath": job_project_folder_path,
            **kwargs,
        }
        return await self.request(
            RequestEnums.POST.value, self._build_url("jobs"), json=body
        )

    async def write_job_data(self, jobid: str, nodes: dict, **kwargs):
        # TODO not sure what the body for the keys mentioned in the V1 doc looks like entirely
        body = {"nodes": nodes, **kwargs}
        return await self.request(
            RequestEnums.PUT.value, self._build_url(f"jobs/{jobid}"), json=body
        )

    async def create_node(
        self, jobid: str, latitude: float, longitude: float, attributes: dict
    ) -> Response:
        return await self.request(
            RequestEnums.POST.value,
            self._build_url(f"jobs/{jobid}/nodes"),
            json={
                "latitude": latitude,
                "longitude": longitude,
                "attributes": [
                    {"attribute": key, "value": value}
                    for key, value in attributes.items()
                ],
            },
        )

    async def delete_node(self, jobid: str, nodeid: str) -> Response:
        return await self.request(
            RequestEnums.DELETE.value, self._build_url(f"jobs/{jobid}/nodes/{nodeid}")
        )

    def _build_url(self, endpoint: str) -> str:
        return urljoin(self._base_url, endpoint)
