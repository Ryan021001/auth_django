import logging

from rest_framework.response import Response
from rest_framework.exceptions import APIException as RestAPIException
from jwt import PyJWTError

from common.error_codes import *  # noqa: F403 # pylint: disable=wildcard-import,unused-wildcard-import

logger = logging.getLogger(__file__)


def http_status_message(status_code):
    return HTTP_STATUS_CODES.get(status_code, '')


def error_data(error_code, error_message, error_detail: any = None):
    if error_detail:
        error_message = None
    error = {
        'error_code': error_code,
        'error_message': error_message or '',
        'error_detail': error_detail or {}
    }
    return error


class APIException(Exception):
    status_code = 500
    http_status_code = HTTP_500_INTERNAL_SERVER_ERROR
    params = []

    def __init__(self, error_code=None, error_message: str = None, error_detail: any = None,
                 *args):  # pylint: disable=keyword-arg-before-vararg
        if error_code in self.http_status_code:
            self.error_code = error_code
        else:
            self.error_code = self.status_code
        if not error_message:
            error_message = self.http_status_code.get(error_code, http_status_message(self.status_code))
            error_message = error_message.format(*args) if not error_detail else None
        self.error_message = error_message
        self.error_detail = error_detail

    @property
    def description(self):
        return error_data(self.error_code, self.error_message, self.error_detail)


class BadRequest(APIException):
    status_code = 400
    http_status_code = HTTP_400_BAD_REQUEST


class Unauthorized(APIException):
    status_code = 401
    http_status_code = HTTP_401_UNAUTHORIZED


class Forbidden(APIException):
    status_code = 403
    http_status_code = HTTP_403_FORBIDDEN


class NotFound(APIException):
    status_code = 404
    http_status_code = HTTP_404_NOT_FOUND


class MethodNotAllowed(APIException):
    status_code = 405
    http_status_code = HTTP_405_METHOD_NOT_ALLOWED


class NotAcceptable(APIException):
    status_code = 406
    http_status_code = HTTP_406_NOT_ACCEPTABLE


class Conflict(APIException):
    status_code = 409
    http_status_code = HTTP_409_CONFLICT


class OverLimit(APIException):
    status_code = 413
    http_status_code = HTTP_413_REQUEST_ENTITY_TOO_LARGE


class UnsupportedMediaType(APIException):
    status_code = 415
    http_status_code = HTTP_415_UNSUPPORTED_MEDIA_TYPE


class UnprocessableEntity(APIException):
    status_code = 422
    http_status_code = HTTP_422_UNPROCESSABLE_ENTITY


class RateLimit(APIException):
    status_code = 429
    http_status_code = HTTP_429_TOO_MANY_REQUESTS


class InternalServerError(APIException):
    status_code = 500
    http_status_code = HTTP_500_INTERNAL_SERVER_ERROR


def api_error_handler(error, exc):  # pylint: disable=unused-argument
    if isinstance(error, APIException):
        error_code = error.status_code
    elif isinstance(error, RestAPIException):
        error_code = error.status_code
        error_message = error.detail if isinstance(error.detail, str) else None
        error_detail = error.detail if not isinstance(error.detail, str) else None
        error.description = error_data(error_code=error_code, error_message=error_message, error_detail=error_detail)
    elif isinstance(error, PyJWTError):
        error_code = 401
        error = Unauthorized(401000, str(error))
    else:
        error_code = 500
        error.description = error_data(error_code=error_code, error_message=http_status_message(error_code))
    msg = f'HTTP_STATUS_CODE_{error_code}: {error.description}'
    if error_code != 404:
        logger.error(msg, exc_info=error)
    return Response(error.description, error_code)
