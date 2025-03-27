import asyncio
import unittest

from katapult_api.utils import task_handler


class TestTaskHandler(unittest.IsolatedAsyncioTestCase):
    async def mock_async_func(self, *args, **kwargs) -> int:
        """Mock async request"""
        await asyncio.sleep(0.1)
        return 1

    async def test_task_handler(self):
        param_list = [{"param": i} for i in range(3)]
        results = await task_handler(self.mock_async_func, param_list=param_list)

        for result in results:
            self.assertEqual(result, 1)

    async def test_task_handler_no_params(self):
        results = await task_handler(self.mock_async_func, param_list=None)

        for result in results:
            self.assertEqual(result, 1)


if __name__ == "__main__":
    unittest.main()
