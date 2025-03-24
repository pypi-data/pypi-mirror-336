# miarec_s3fs

[![Actions](https://img.shields.io/github/actions/workflow/status/miarec/miarec_s3fs/test_and_release.yml?branch=master&logo=github&style=flat-square&maxAge=300)](https://github.com/miarec/miarec_s3fs/actions)

MiaRec S3FS is a [PyFilesystem](https://www.pyfilesystem.org/) interface to
Amazon S3 cloud storage.

As a PyFilesystem concrete class, [S3FS](http://fs-s3fs.readthedocs.io/en/latest/) allows you to work with S3 in the
same way as any other supported filesystem.

This a fork of the [fs-s3fs](https://github.com/PyFilesystem/s3fs) project, written by Will McGugan (email willmcgugan@gmail.com). 

The code was modified by MiaRec team to fullfill out needs.

## Notable differences between miarec_s3fs and fs-s3fs

1. Required Python 3.6+. A support of Python 2.7 is removed.

2. Opener is not implemented. Use explicit constructor instead.

3. Unit tests are run with [moto](https://github.com/getmoto/moto)


## Installing

You can install S3FS from pip as follows:

```
pip install miarec_s3fs
```

This will install the most recent stable version.

Alternatively, if you want the cutting edge code, you can check out
the GitHub repos at https://github.com/miarec/miarec_s3fs

## Opening a S3FS

Open an S3FS by explicitly using the constructor:

```python
from fs_s3fs import S3FS
s3fs = S3FS('mybucket')
```

## Limitations

Amazon S3 isn't strictly speaking a *filesystem*, in that it contains
files, but doesn't offer true *directories*. S3FS follows the convention
of simulating directories by creating an object that ends in a forward
slash. For instance, if you create a file called `"foo/bar"`, S3FS will
create an S3 object for the file called `"foo/bar"` *and* an
empty object called `"foo/"` which stores that fact that the `"foo"`
directory exists.

If you create all your files and directories with S3FS, then you can
forget about how things are stored under the hood. Everything will work
as you expect. You *may* run in to problems if your data has been
uploaded without the use of S3FS. For instance, if you create a
`"foo/bar"` object without a `"foo/"` object. If this occurs, then S3FS
may give errors about directories not existing, where you would expect
them to be. The solution is to create an empty object for all
directories and subdirectories. Fortunately most tools will do this for
you, and it is probably only required of you upload your files manually.

## Authentication

If you don't supply any credentials, then S3FS will use the access key
and secret key configured on your system. 

Here's how you specify credentials with the constructor:

    s3fs = S3FS(
        'mybucket'
        aws_access_key_id=<access key>,
        aws_secret_access_key=<secret key>
    )

Note: Amazon recommends against specifying credentials explicitly like this in production.


## Downloading Files

To *download* files from an S3 bucket, open a file on the S3
filesystem for reading, then write the data to a file on the local
filesystem. Here's an example that copies a file `example.mov` from
S3 to your HD:

```python
from fs.tools import copy_file_data
with s3fs.open('example.mov', 'rb') as remote_file:
    with open('example.mov', 'wb') as local_file:
        copy_file_data(remote_file, local_file)
```

Although it is preferable to use the higher-level functionality in the
`fs.copy` module. Here's an example:

```python
from fs.copy import copy_file
copy_file(s3fs, 'example.mov', './', 'example.mov')
```

## Uploading Files

You can *upload* files in the same way. Simply copy a file from a
source filesystem to the S3 filesystem.
See [Moving and Copying](https://docs.pyfilesystem.org/en/latest/guide.html#moving-and-copying)
for more information.

## ExtraArgs

S3 objects have additional properties, beyond a traditional
filesystem. These options can be set using the ``upload_args``
and ``download_args`` properties. which are handed to upload
and download methods, as appropriate, for the lifetime of the
filesystem instance.

For example, to set the ``cache-control`` header of all objects
uploaded to a bucket:

```python
import fs, fs.mirror
s3fs = S3FS('example', upload_args={"CacheControl": "max-age=2592000", "ACL": "public-read"})
fs.mirror.mirror('/path/to/mirror', s3fs)
```

see [the Boto3 docs](https://boto3.readthedocs.io/en/latest/reference/customizations/s3.html#boto3.s3.transfer.S3Transfer.ALLOWED_UPLOAD_ARGS)
for more information.

## S3 Info

You can retrieve S3 info via the ``s3`` namespace. Here's an example:

```python
>>> info = s.getinfo('foo', namespaces=['s3'])
>>> info.raw['s3']
{'metadata': {}, 'delete_marker': None, 'version_id': None, 'parts_count': None, 'accept_ranges': 'bytes', 'last_modified': 1501935315, 'content_length': 3, 'content_encoding': None, 'request_charged': None, 'replication_status': None, 'server_side_encryption': None, 'expires': None, 'restore': None, 'content_type': 'binary/octet-stream', 'sse_customer_key_md5': None, 'content_disposition': None, 'storage_class': None, 'expiration': None, 'missing_meta': None, 'content_language': None, 'ssekms_key_id': None, 'sse_customer_algorithm': None, 'e_tag': '"37b51d194a7513e45b56f6524f2d51f2"', 'website_redirect_location': None, 'cache_control': None}
```


## S3 URLs

You can use the ``geturl`` method to generate an externally accessible
URL from an S3 object. Here's an example:

```python
>>> s3fs.geturl('foo')
'https://fsexample.s3.amazonaws.com//foo?AWSAccessKeyId=AKIAIEZZDQU72WQP3JUA&Expires=1501939084&Signature=4rfDuqVgmvILjtTeYOJvyIXRMvs%3D'
```

## Testing

Automated unit tests are run on [GitHub Actions](https://github.com/miarec/miarec_s3fs/actions)

To run the tests locally, do the following.

Install Docker on local machine.

Create activate python virtual environment:

    python -m vevn venv
    source venv\bin\activate

Install the project and test dependencies:

    pip install -e ".[test]"

Run tests:

    pytest

## Documentation

- [PyFilesystem Wiki](https://www.pyfilesystem.org)
- [PyFilesystem Reference](https://docs.pyfilesystem.org/en/latest/reference/base.html)
