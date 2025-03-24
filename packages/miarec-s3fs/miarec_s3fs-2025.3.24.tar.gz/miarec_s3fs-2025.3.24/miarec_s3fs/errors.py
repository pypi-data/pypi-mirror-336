
import contextlib
from ssl import SSLError
from botocore.exceptions import ClientError, EndpointConnectionError

from fs import errors


@contextlib.contextmanager
def s3errors(path):
    """Translate S3 errors to FSErrors."""
    try:
        yield
    except ClientError as error:
        _error = error.response.get("Error", {})
        error_code = _error.get("Code", None)
        response_meta = error.response.get("ResponseMetadata", {})
        http_status = response_meta.get("HTTPStatusCode", 200)
        error_msg = _error.get("Message", None)
        if error_code == "NoSuchBucket":
            raise errors.ResourceError(path, exc=error, msg=error_msg)
        if http_status == 404:
            raise errors.ResourceNotFound(path)
        elif http_status == 403:
            raise errors.PermissionDenied(path=path, msg=error_msg)
        else:
            raise errors.OperationFailed(path=path, exc=error)
    except SSLError as error:
        raise errors.OperationFailed(path, exc=error)
    except EndpointConnectionError as error:
        raise errors.RemoteConnectionError(path, exc=error, msg="{}".format(error))
