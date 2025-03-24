import os
import unittest
from moto import mock_aws as mock_s3

from fs.test import FSTestCases
from miarec_s3fs import S3FS

import boto3


class TestS3FSHelpers(unittest.TestCase):
    def test_path_to_key(self):
        s3 = S3FS("foo")
        self.assertEqual(s3._path_to_key("foo.bar"), "foo.bar")
        self.assertEqual(s3._path_to_key("foo/bar"), "foo/bar")

    def test_path_to_key_subdir(self):
        s3 = S3FS("foo", "/dir")
        self.assertEqual(s3._path_to_key("foo.bar"), "dir/foo.bar")
        self.assertEqual(s3._path_to_key("foo/bar"), "dir/foo/bar")

    def test_upload_args(self):
        s3 = S3FS("foo", acl="acl", cache_control="cc")
        self.assertDictEqual(
            s3._get_upload_args("test.jpg"),
            {"ACL": "acl", "CacheControl": "cc", "ContentType": "image/jpeg"},
        )
        self.assertDictEqual(
            s3._get_upload_args("test.mp3"),
            {"ACL": "acl", "CacheControl": "cc", "ContentType": "audio/mpeg"},
        )
        self.assertDictEqual(
            s3._get_upload_args("test.json"),
            {"ACL": "acl", "CacheControl": "cc", "ContentType": "application/json"},
        )
        self.assertDictEqual(
            s3._get_upload_args("unknown.unknown"),
            {"ACL": "acl", "CacheControl": "cc", "ContentType": "binary/octet-stream"},
        )


class S3FSTestCases(FSTestCases):
    """Base class that initializes S3 testing environment with Moto mocking library"""

    bucket_name = "testing"

    def setUp(self):
        super().setUp()

        # Mocked AWS Credentials for moto
        # This will elimitate a posibility of mutating real AWS environment
        os.environ["AWS_ACCESS_KEY_ID"] = "testing"
        os.environ["AWS_SECRET_ACCESS_KEY"] = "testing"
        os.environ["AWS_SECURITY_TOKEN"] = "testing"
        os.environ["AWS_SESSION_TOKEN"] = "testing"
        os.environ["AWS_DEFAULT_REGION"] = "us-east-1"

        # Mock S3 with Moto
        self.mock_s3 = mock_s3()
        self.mock_s3.start()

        self.s3 = boto3.resource("s3")
        self.client = boto3.client("s3")

        # Create a testing bucket
        bucket = self.s3.Bucket(self.bucket_name)
        bucket.create()


    def tearDown(self):
        self.mock_s3.stop()
        super().tearDown()


class TestS3FS(S3FSTestCases, unittest.TestCase):
    """Test S3FS implementation in a root path"""

    def make_fs(self):
        return S3FS(self.bucket_name)


class TestS3FSSubDir(S3FSTestCases, unittest.TestCase):
    """Test S3FS implementation in a sub-directory"""

    def setUp(self):
        super().setUp()
        self.s3.Object(self.bucket_name, "subdirectory").put()

    def make_fs(self):
        return S3FS(self.bucket_name, dir_path="subdirectory")

