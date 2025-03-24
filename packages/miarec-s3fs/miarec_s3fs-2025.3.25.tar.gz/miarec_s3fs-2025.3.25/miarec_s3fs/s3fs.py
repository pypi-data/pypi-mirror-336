
from datetime import datetime
import io
import itertools
import os
import threading
import mimetypes

import boto3
from botocore.config import Config

from fs import ResourceType
from fs.base import FS
from fs.info import Info
from fs import errors
from fs.mode import Mode
from fs.subfs import SubFS
from fs.path import basename, dirname, forcedir, join, normpath, relpath
from fs.time import datetime_to_epoch


from .s3file import S3File
from .helpers import _make_repr
from .errors import s3errors



class S3FS(FS):
    """
    Construct an Amazon S3 filesystem for
    `PyFilesystem <https://pyfilesystem.org>`_

    :param str bucket_name: The S3 bucket name.
    :param str dir_path: The root directory within the S3 Bucket.
        Defaults to ``"/"``
    :param str aws_access_key_id: The access key, or ``None`` to read
        the key from standard configuration files.
    :param str aws_secret_access_key: The secret key, or ``None`` to
        read the key from standard configuration files.
    :param str endpoint_url: Alternative endpoint url (``None`` to use
        default).
    :param str aws_session_token:
    :param str region: Optional S3 region.
    :param bool strict: When ``True`` (default) S3FS will follow the
        PyFilesystem specification exactly. Set to ``False`` to disable
        validation of destination paths which may speed up uploads /
        downloads.
    :param str cache_control: Sets the 'Cache-Control' header for uploads.
    :param str acl: Sets the Access Control List header for uploads.
    :param dict upload_args: A dictionary for additional upload arguments.
        See https://boto3.readthedocs.io/en/latest/reference/services/s3.html#S3.Object.put
        for details.
    :param dict download_args: Dictionary of extra arguments passed to
        the S3 client.
    :param dict config_args: Advanced S3 client configuration options.
        See https://botocore.amazonaws.com/v1/documentation/api/latest/reference/config.html
    """

    _meta = {
        "case_insensitive": False,
        "invalid_path_chars": "\0",
        "network": True,
        "read_only": False,
        "thread_safe": True,
        "unicode_paths": True,
        "virtual": False,
    }

    _object_attributes = [
        "accept_ranges",
        "cache_control",
        "content_disposition",
        "content_encoding",
        "content_language",
        "content_length",
        "content_type",
        "delete_marker",
        "e_tag",
        "expiration",
        "expires",
        "last_modified",
        "metadata",
        "missing_meta",
        "parts_count",
        "replication_status",
        "request_charged",
        "restore",
        "server_side_encryption",
        "sse_customer_algorithm",
        "sse_customer_key_md5",
        "ssekms_key_id",
        "storage_class",
        "version_id",
        "website_redirect_location",
    ]

    def __init__(
        self,
        bucket_name,
        dir_path="/",
        aws_access_key_id=None,
        aws_secret_access_key=None,
        aws_session_token=None,
        endpoint_url=None,
        region=None,
        strict=True,
        cache_control=None,
        acl=None,
        upload_args=None,
        download_args=None,
        config_args=None,
    ):
        _creds = (aws_access_key_id, aws_secret_access_key)
        if any(_creds) and not all(_creds):
            raise ValueError(
                "aws_access_key_id and aws_secret_access_key "
                "must be set together if specified"
            )
        self._bucket_name = bucket_name
        self.dir_path = dir_path
        self._prefix = relpath(normpath(dir_path)).rstrip("/")
        self.aws_access_key_id = aws_access_key_id
        self.aws_secret_access_key = aws_secret_access_key
        self.aws_session_token = aws_session_token
        self.endpoint_url = endpoint_url
        self.region = region
        self.strict = strict
        self._tlocal = threading.local()
        if cache_control or acl:
            upload_args = upload_args or {}
            if cache_control:
                upload_args["CacheControl"] = cache_control
            if acl:
                upload_args["ACL"] = acl
        self.upload_args = upload_args
        self.download_args = download_args
        self.config_args = config_args
        super(S3FS, self).__init__()

    def __repr__(self):
        return _make_repr(
            self.__class__.__name__,
            self._bucket_name,
            dir_path=(self.dir_path, "/"),
            region=(self.region, None),
        )

    def __str__(self):
        return "<s3fs '{}'>".format(join(self._bucket_name, relpath(self.dir_path)))

    def _path_to_key(self, path):
        """Converts an fs path to a s3 key."""
        _path = relpath(normpath(path))
        _key = (
            "{}/{}".format(self._prefix, _path).lstrip("/")
        )
        return _key

    def _path_to_dir_key(self, path):
        """Converts an fs path to a s3 key."""
        _path = relpath(normpath(path))
        _key = (
            forcedir("{}/{}".format(self._prefix, _path))
            .lstrip("/")
        )
        return _key

    def _key_to_path(self, key):
        return key

    def _get_object(self, path, key, try_dir=True):
        try:
            with s3errors(path):
                obj = self.s3.Object(self._bucket_name, key)
                obj.load()
        except errors.ResourceNotFound:
            if try_dir and not key.endswith("/"):
                with s3errors(path):
                    obj = self.s3.Object(self._bucket_name, key + "/")
                    obj.load()
                    return obj
            else:
                raise
        else:
            return obj

    def _get_upload_args(self, key):
        upload_args = self.upload_args.copy() if self.upload_args else {}
        if "ContentType" not in upload_args:
            mime_type, _encoding = mimetypes.guess_type(key)
            upload_args["ContentType"] = mime_type or "binary/octet-stream"
        return upload_args

    @property
    def s3_session(self):
        if not hasattr(self._tlocal, 's3_session'):
            self._tlocal.s3_session = boto3.Session()
        return self._tlocal.s3_session

    @property
    def s3(self):
        config = Config(**self.config_args) if self.config_args else None
        if not hasattr(self._tlocal, "s3"):
            self._tlocal.s3 = self.s3_session.resource(
                "s3",
                region_name=self.region,
                aws_access_key_id=self.aws_access_key_id,
                aws_secret_access_key=self.aws_secret_access_key,
                aws_session_token=self.aws_session_token,
                endpoint_url=self.endpoint_url,
                config=config,
            )
        return self._tlocal.s3

    @property
    def client(self):
        if not hasattr(self._tlocal, "client"):
            config = Config(**self.config_args) if self.config_args else None
            self._tlocal.client = self.s3_session.client(
                "s3",
                region_name=self.region,
                aws_access_key_id=self.aws_access_key_id,
                aws_secret_access_key=self.aws_secret_access_key,
                aws_session_token=self.aws_session_token,
                endpoint_url=self.endpoint_url,
                config=config,
            )
        return self._tlocal.client

    def _info_from_object(self, obj, namespaces):
        """Make an info dict from an s3 Object."""
        key = obj.key
        path = self._key_to_path(key)
        name = basename(path.rstrip("/"))
        is_dir = key.endswith("/")
        info = {"basic": {"name": name, "is_dir": is_dir}}
        if "details" in namespaces:
            _type = int(ResourceType.directory if is_dir else ResourceType.file)
            info["details"] = {
                "accessed": None,
                "modified": datetime_to_epoch(obj.last_modified),
                "size": obj.content_length,
                "type": _type,
            }
        if "s3" in namespaces:
            s3info = info["s3"] = {}
            for name in self._object_attributes:
                value = getattr(obj, name, None)
                if isinstance(value, datetime):
                    value = datetime_to_epoch(value)
                s3info[name] = value
        if "urls" in namespaces:
            url = self.client.generate_presigned_url(
                ClientMethod="get_object",
                Params={"Bucket": self._bucket_name, "Key": key},
            )
            info["urls"] = {"download": url}
        return info

    def isdir(self, path):
        _path = self.validatepath(path)
        if self.strict or not _path.endswith("/"):
            try:
                return self._getinfo(forcedir(_path)).is_dir
            except errors.ResourceNotFound:
                return False
        else:
            return _path.endswith("/") or _path == ""

    def getinfo(self, path, namespaces=None):
        self.check()
        namespaces = namespaces or ()
        _path = self.validatepath(path)
        _key = self._path_to_key(_path)

        if self.strict:
            # Check the parent directory
            # Disabled due to performance penalty and low value (c) MiaRec
            try:
                dir_path = dirname(_path)
                if dir_path != "/":
                    _dir_key = self._path_to_dir_key(dir_path)
                    with s3errors(path):
                        obj = self.s3.Object(self._bucket_name, _dir_key)
                        obj.load()
            except errors.ResourceNotFound:
                raise errors.ResourceNotFound(path)
        if _path == "/":
            return Info(
                {
                    "basic": {"name": "", "is_dir": True},
                    "details": {"type": int(ResourceType.directory)},
                }
            )

        obj = self._get_object(path, _key, try_dir=True)
        info = self._info_from_object(obj, namespaces)
        return Info(info)

    def _getinfo(self, path, namespaces=None):
        """Gets info without checking for parent dir."""
        namespaces = namespaces or ()
        _path = self.validatepath(path)
        _key = self._path_to_key(_path)
        if _path == "/":
            return Info(
                {
                    "basic": {"name": "", "is_dir": True},
                    "details": {"type": int(ResourceType.directory)},
                }
            )

        obj = self._get_object(path, _key, try_dir=True)
        info = self._info_from_object(obj, namespaces)
        return Info(info)

    def listdir(self, path):
        _path = self.validatepath(path)
        _s3_key = self._path_to_dir_key(_path)
        prefix_len = len(_s3_key)

        paginator = self.client.get_paginator("list_objects")
        with s3errors(path):
            _paginate = paginator.paginate(
                Bucket=self._bucket_name, Prefix=_s3_key, Delimiter="/"
            )
            _directory = []
            for result in _paginate:
                common_prefixes = result.get("CommonPrefixes", ())
                for prefix in common_prefixes:
                    _prefix = prefix.get("Prefix")
                    _name = _prefix[prefix_len:]
                    if _name:
                        _directory.append(_name.rstrip("/"))
                for obj in result.get("Contents", ()):
                    name = obj["Key"][prefix_len:]
                    if name:
                        _directory.append(name)

        if not _directory:
            if not self.getinfo(_path).is_dir:
                raise errors.DirectoryExpected(path)

        return _directory

    def opendir(self, path, factory=None):
        return super().opendir(forcedir(path), factory=factory)

    def makedir(self, path, permissions=None, recreate=False):
        self.check()
        _path = self.validatepath(path)
        _key = self._path_to_dir_key(_path)

        if self.strict:
            # Check existence of the parent directory (slow)
            if not self.isdir(dirname(_path)):
                raise errors.ResourceNotFound(path)

        # Do we need to create a fake object for the directory? (c) MiaRec
        # We probably can always return True from makedir()
        # And isdir() should return True only if there are files under the path (slow).
        # Or isdir() should always return True if path ends with "/"

        try:
            self._getinfo(forcedir(path))
        except errors.ResourceNotFound:
            pass
        else:
            if recreate:
                return self.opendir(_path)
            else:
                raise errors.DirectoryExists(path)
        with s3errors(path):
            _obj = self.s3.Object(self._bucket_name, _key)
            _obj.put(**self._get_upload_args(_key))
        return SubFS(self, path)

    def openbin(self, path, mode="rb", buffering=-1, **options):
        _mode = Mode(mode)
        _mode.validate_bin()
        self.check()
        _path = self.validatepath(path)
        _key = self._path_to_key(_path)

        if _mode.create:

            def on_close_create(s3file):
                """Called when the S3 file closes, to upload data."""
                try:
                    s3file.raw.seek(0)
                    with s3errors(path):
                        self.client.upload_fileobj(
                            s3file.raw,
                            self._bucket_name,
                            _key,
                            ExtraArgs=self._get_upload_args(_key),
                        )
                finally:
                    s3file.raw.close()

            if self.strict:
                # Check of the parent directory is disabled due to performance penalty
                try:
                    dir_path = dirname(_path)
                    if dir_path != "/":
                        _dir_key = self._path_to_dir_key(dir_path)
                        self._get_object(dir_path, _dir_key, try_dir=False)
                except errors.ResourceNotFound:
                    raise errors.ResourceNotFound(path)

            try:
                info = self._getinfo(path)
            except errors.ResourceNotFound:
                pass
            else:
                if _mode.exclusive:
                    raise errors.FileExists(path)
                if info.is_dir:
                    raise errors.FileExpected(path)

            s3file = S3File.factory(
                path, 
                _mode.to_platform_bin(), 
                on_close=on_close_create
            )
            if _mode.appending:
                try:
                    with s3errors(path):
                        self.client.download_fileobj(
                            self._bucket_name,
                            _key,
                            s3file.raw,
                            ExtraArgs=self.download_args,
                        )
                except errors.ResourceNotFound:
                    pass
                else:
                    s3file.seek(0, os.SEEK_END)

            return s3file

        if self.strict:
            info = self.getinfo(path)
            if info.is_dir:
                raise errors.FileExpected(path)

        def on_close(s3file):
            """Called when the S3 file closes, to upload the data."""
            try:
                if _mode.writing:
                    s3file.raw.seek(0, os.SEEK_SET)
                    with s3errors(path):
                        self.client.upload_fileobj(
                            s3file.raw,
                            self._bucket_name,
                            _key,
                            ExtraArgs=self._get_upload_args(_key),
                        )
            finally:
                s3file.raw.close()

        s3file = S3File.factory(
            path, 
            _mode.to_platform_bin(), 
            on_close=on_close
        )
        with s3errors(path):
            self.client.download_fileobj(
                self._bucket_name, _key, s3file.raw, ExtraArgs=self.download_args
            )
        s3file.seek(0, os.SEEK_SET)
        return s3file

    def remove(self, path):
        self.check()
        _path = self.validatepath(path)
        _key = self._path_to_key(_path)
        if self.strict:
            info = self.getinfo(path)
            if info.is_dir:
                raise errors.FileExpected(path)
        elif _path.endswith("/") or not _path:
            raise errors.FileExpected(path)
        with s3errors(path):
            self.client.delete_object(Bucket=self._bucket_name, Key=_key)

    def isempty(self, path):
        self.check()
        _path = self.validatepath(path)
        _key = self._path_to_dir_key(_path)
        response = self.client.list_objects(
            Bucket=self._bucket_name, Prefix=_key, MaxKeys=2
        )
        contents = response.get("Contents", ())
        for obj in contents:
            if obj["Key"] != _key:
                return False
        return True

    def removedir(self, path):
        self.check()
        _path = self.validatepath(path)
        if _path == "/":
            raise errors.RemoveRootError()
        if self.strict:
            info = self.getinfo(_path)
            if not info.is_dir:
                raise errors.DirectoryExpected(path)
        if not self.isempty(path):
            raise errors.DirectoryNotEmpty(path)
        _key = self._path_to_dir_key(_path)
        try:
            with s3errors(path):
                self.client.delete_object(Bucket=self._bucket_name, Key=_key)
        except errors.ResourceNotFound:
            # Directory is a virtual concept in S3. 
            # There can be a directory object with "/" and the end of name, but this is optional
            pass   

    def setinfo(self, path, info):
        self.getinfo(path)

    def readbytes(self, path):
        self.check()
        if self.strict:
            info = self.getinfo(path)
            if not info.is_file:
                raise errors.FileExpected(path)
        _path = self.validatepath(path)
        _key = self._path_to_key(_path)
        bytes_file = io.BytesIO()
        with s3errors(path):
            self.client.download_fileobj(
                self._bucket_name, _key, bytes_file, ExtraArgs=self.download_args
            )
        return bytes_file.getvalue()

    def download(self, path, file, chunk_size=None, **options):
        self.check()
        if self.strict:
            info = self.getinfo(path)
            if not info.is_file:
                raise errors.FileExpected(path)
        _path = self.validatepath(path)
        _key = self._path_to_key(_path)
        with s3errors(path):
            self.client.download_fileobj(
                self._bucket_name, _key, file, ExtraArgs=self.download_args
            )

    def exists(self, path):
        self.check()
        _path = self.validatepath(path)
        if _path == "/":
            return True
        _key = self._path_to_key(_path)
        try:
            self._get_object(path, _key, try_dir=True)
        except errors.ResourceNotFound:
            return False
        else:
            return True

    def scandir(self, path, namespaces=None, page=None):
        _path = self.validatepath(path)
        namespaces = namespaces or ()
        _s3_key = self._path_to_dir_key(_path)
        prefix_len = len(_s3_key)
        if self.strict:
            info = self.getinfo(path)
            if not info.is_dir:
                raise errors.DirectoryExpected(path)

        paginator = self.client.get_paginator("list_objects")
        _paginate = paginator.paginate(
            Bucket=self._bucket_name, Prefix=_s3_key, Delimiter="/"
        )

        def gen_info():
            for result in _paginate:
                common_prefixes = result.get("CommonPrefixes", ())
                for prefix in common_prefixes:
                    _prefix = prefix.get("Prefix")
                    _name = _prefix[prefix_len:]
                    if _name:
                        info = {
                            "basic": {
                                "name": _name.rstrip("/"),
                                "is_dir": True,
                            }
                        }
                        yield Info(info)
                for _obj in result.get("Contents", ()):
                    name = _obj["Key"][prefix_len:]
                    if name:
                        with s3errors(path):
                            obj = self.s3.Object(self._bucket_name, _obj["Key"])
                        info = self._info_from_object(obj, namespaces)
                        yield Info(info)

        iter_info = iter(gen_info())
        if page is not None:
            start, end = page
            iter_info = itertools.islice(iter_info, start, end)

        for info in iter_info:
            yield info

    def writebytes(self, path, contents):
        if not isinstance(contents, bytes):
            raise TypeError("contents must be bytes")

        _path = self.validatepath(path)
        _key = self._path_to_key(_path)
        if self.strict:
            if not self.isdir(dirname(path)):
                raise errors.ResourceNotFound(path)
            try:
                info = self._getinfo(path)
                if info.is_dir:
                    raise errors.FileExpected(path)
            except errors.ResourceNotFound:
                pass

        bytes_file = io.BytesIO(contents)
        with s3errors(path):
            self.client.upload_fileobj(
                bytes_file,
                self._bucket_name,
                _key,
                ExtraArgs=self._get_upload_args(_key),
            )

    def upload(self, path, file, chunk_size=None, **options):
        _path = self.validatepath(path)
        _key = self._path_to_key(_path)

        if self.strict:
            if not self.isdir(dirname(path)):
                raise errors.ResourceNotFound(path)
            try:
                info = self._getinfo(path)
                if info.is_dir:
                    raise errors.FileExpected(path)
            except errors.ResourceNotFound:
                pass

        with s3errors(path):
            self.client.upload_fileobj(
                file, self._bucket_name, _key, ExtraArgs=self._get_upload_args(_key)
            )

    def copy(self, src_path, dst_path, overwrite=False, preserve_time=False):
        if not overwrite and self.exists(dst_path):
            raise errors.DestinationExists(dst_path)
        _src_path = self.validatepath(src_path)
        _dst_path = self.validatepath(dst_path)
        if self.strict:
            if not self.isdir(dirname(_dst_path)):
                raise errors.ResourceNotFound(dst_path)
        _src_key = self._path_to_key(_src_path)
        _dst_key = self._path_to_key(_dst_path)
        try:
            with s3errors(src_path):
                self.client.copy_object(
                    Bucket=self._bucket_name,
                    Key=_dst_key,
                    CopySource={"Bucket": self._bucket_name, "Key": _src_key},
                    **self._get_upload_args(_src_key)
                )
        except errors.ResourceNotFound:
            if self.exists(src_path):
                raise errors.FileExpected(src_path)
            raise

    def move(self, src_path, dst_path, overwrite=False, preserve_time=False):
        self.copy(src_path, dst_path, overwrite=overwrite, preserve_time=preserve_time)
        self.remove(src_path)

    def geturl(self, path, purpose="download"):
        _path = self.validatepath(path)
        _key = self._path_to_key(_path)
        if _path == "/":
            raise errors.NoURL(path, purpose)
        if purpose == "download":
            url = self.client.generate_presigned_url(
                ClientMethod="get_object",
                Params={"Bucket": self._bucket_name, "Key": _key},
            )
            return url
        else:
            raise errors.NoURL(path, purpose)
