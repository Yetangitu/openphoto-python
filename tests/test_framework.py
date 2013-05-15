import logging
try:
    import unittest2 as unittest # python2.6
except ImportError:
    import unittest

import openphoto
import tests.test_base

class TestFramework(tests.test_base.TestBase):
    testcase_name = "framework"

    def setUp(self):
        """Override the default setUp, since we don't need a populated database"""
        logging.info("\nRunning %s..." % self.id())

    def test_api_version_zero(self):
        # API v0 has a special hello world message
        client = openphoto.OpenPhoto(config_file=self.config_file,
                                     api_version=0)
        result = client.get("hello.json")
        self.assertEqual(result['message'], "Hello, world! This is version zero of the API!")
        self.assertEqual(result['result']['__route__'], "/v0/hello.json")

    def test_specified_api_version(self):
        # For all API versions >0, we get a generic hello world message
        for api_version in range(1, tests.test_base.get_test_server_api() + 1):
            client = openphoto.OpenPhoto(config_file=self.config_file,
                                         api_version=api_version)
            result = client.get("hello.json")
            self.assertEqual(result['message'], "Hello, world!")
            self.assertEqual(result['result']['__route__'], "/v%d/hello.json" % api_version)

    def test_unspecified_api_version(self):
        # If the API version is unspecified, we get a generic hello world message
        client = openphoto.OpenPhoto(config_file=self.config_file,
                                     api_version=None)
        result = client.get("hello.json")
        self.assertEqual(result['message'], "Hello, world!")
        self.assertEqual(result['result']['__route__'], "/hello.json")

    def test_future_api_version(self):
        # If the API version is unsupported, we should get an error
        # (it's a ValueError, since the returned 404 HTML page is not valid JSON)
        client = openphoto.OpenPhoto(config_file=self.config_file,
                                     api_version=openphoto.LATEST_API_VERSION + 1)
        with self.assertRaises(openphoto.OpenPhoto404Error):
            client.get("hello.json")
