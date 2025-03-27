import json
import unittest

from katapult_api.structs.response import Response


class TestResponse(unittest.TestCase):
    def test_response_json_decode_success(self):
        content = {"body": "success"}

        response = Response(1, 0, None, json.dumps(content))
        self.assertEqual(response.json(), content)

    def test_response_json_decode_failures(self):
        test_cases = ["not json", "", None]

        for content in test_cases:
            with self.subTest(content=content):
                response = Response(1, 0, None, content)
                with self.assertRaises((json.JSONDecodeError, TypeError)):
                    response.json()
