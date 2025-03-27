import asyncio
import unittest
from unittest.mock import AsyncMock, patch

from katapult_api.client import Client
from katapult_api.enums import RequestEnums
from katapult_api.utils import task_handler


class TestClient(unittest.IsolatedAsyncioTestCase):
    TEST_API_KEY = "test_key"
    TEST_BASE_URL = "test_url"

    def get_mock_request(self, content: str = '{"body":"success"}', status: int = 200):
        """Returns a mock request method with customizable content and status"""

        async def mock_request(*args, **kwargs) -> tuple[str, str, int]:
            await asyncio.sleep(2)

            mock_response = AsyncMock()
            mock_response.content = content
            mock_response.headers = f'{{"content-length":{len(content)}}}'
            mock_response.status = status

            return mock_response.content, mock_response.headers, mock_response.status

        return mock_request

    async def test_various_methods_and_responses(self):
        """Test multiple response scenarios across different HTTP methods"""
        test_cases = [
            # Success cases
            {
                "method": "GET",
                "content": '{"body":"success"}',
                "status": 200,
                "expected_status": 200,
            },
            {
                "method": "POST",
                "content": '{"body":"created"}',
                "status": 201,
                "expected_status": 201,
            },
            {
                "method": "PUT",
                "content": '{"body":"updated"}',
                "status": 200,
                "expected_status": 200,
            },
            {
                "method": "PATCH",
                "content": '{"body":"patched"}',
                "status": 200,
                "expected_status": 200,
            },
            {
                "method": "DEL",
                "content": '{"body":"deleted"}',
                "status": 204,
                "expected_status": 204,
            },
            # Failure cases
            {
                "method": "GET",
                "content": '{"error":"not found"}',
                "status": 404,
                "expected_status": 404,
            },
            {
                "method": "POST",
                "content": '{"error":"bad request"}',
                "status": 400,
                "expected_status": 400,
            },
            {"method": "PUT", "content": "", "status": 500, "expected_status": 500},
            {
                "method": "PATCH",
                "content": '{"message":"rate limit exceeded"}',
                "status": 429,
                "expected_status": 429,
            },
        ]

        client = Client(self.TEST_BASE_URL, self.TEST_API_KEY, 1)

        for case in test_cases:
            with self.subTest(
                method=case["method"], content=case["content"], status=case["status"]
            ):
                with patch.object(
                    client,
                    "_request",
                    side_effect=self.get_mock_request(
                        content=case["content"], status=case["status"]
                    ),
                ):
                    async with client:
                        response = await client.request(case["method"], "")

                self.assertEqual(response.status, case["expected_status"])
                self.assertEqual(response.content, case["content"])

    async def test_multiple_request(self):
        client = Client(self.TEST_BASE_URL, self.TEST_API_KEY, 1)

        param_list = [{"method": RequestEnums.GET.value, "url": ""} for _ in range(3)]

        with patch.object(client, "_request", side_effect=self.get_mock_request()):
            async with client:
                responses = await task_handler(client.request, param_list=param_list)

        for response in responses:
            self.assertEqual(response.status, 200)
            self.assertEqual(response.content, '{"body":"success"}')

    async def test_session_cleanup(self):
        client = Client(self.TEST_BASE_URL, self.TEST_API_KEY, 1)

        with patch.object(client, "_request", side_effect=self.get_mock_request()):
            async with client:
                await client.request(RequestEnums.GET.value, "")

        self.assertEqual(client._session, None)


class TestClientConcurrency(unittest.IsolatedAsyncioTestCase):
    TEST_API_KEY = "test_key"
    TEST_BASE_URL = "test_url"
    SEMAPHORE_LIMIT = 10

    def setUp(self):
        self.active_requests = 0
        self.max_concurrent = 0

    async def mock_delayed_request(self, *args, **kwargs):
        """Mock request that simulates a delay to observe concurrency"""
        self.active_requests += 1  # Track how many requests are running
        self.max_concurrent = max(self.max_concurrent, self.active_requests)

        await asyncio.sleep(0.5)  # Simulate network delay

        self.active_requests -= 1  # Decrement active count when finished
        return '{"body":"success"}', "{}", 200

    async def test_concurrent_requests_respect_semaphore(self):
        """Ensure concurrent requests never exceed the set semaphore limit"""
        client = Client(self.TEST_BASE_URL, self.TEST_API_KEY, self.SEMAPHORE_LIMIT)
        param_list = [{"method": RequestEnums.GET.value, "url": ""} for _ in range(15)]

        self.active_requests = 0
        self.max_concurrent = 0  # Track the highest concurrent request count

        with patch.object(client, "_request", side_effect=self.mock_delayed_request):
            async with client:
                await task_handler(client.request, param_list=param_list)

        self.assertLessEqual(
            self.max_concurrent,
            self.SEMAPHORE_LIMIT,
            f"Exceeded max concurrency: {self.max_concurrent} > {self.SEMAPHORE_LIMIT}",
        )
