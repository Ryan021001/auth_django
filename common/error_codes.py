from django.utils.translation import gettext_lazy as _

HTTP_STATUS_CODES = {
    100: _("Continue."),
    101: _("Switching Protocols."),
    102: _("Processing."),

    200: _("OK."),
    201: _("Created."),
    202: _("Accepted."),
    203: _("Non Authoritative Information."),
    204: _("No Content."),
    205: _("Reset Content."),
    206: _("Partial Content."),
    207: _("Multi Status."),
    226: _("IM Used."),  # see RFC 3229

    300: _("Multiple Choices."),
    301: _("Moved Permanently."),
    302: _("Found."),
    303: _("See Other."),
    304: _("Not Modified."),
    305: _("Use Proxy."),
    307: _("Temporary Redirect."),

    400: _("Bad Request."),
    401: _("Unauthorized."),
    402: _("Payment Required."),
    403: _("Forbidden."),
    404: _("Not Found."),
    405: _("Method Not Allowed."),
    406: _("Not Acceptable."),
    407: _("Proxy Authentication Required."),
    408: _("Request Timeout."),
    409: _("Conflict."),
    410: _("Gone."),
    411: _("Length Required."),
    412: _("Precondition Failed."),
    413: _("Request Entity Too Large."),
    414: _("Request URI Too Long."),
    415: _("Unsupported Media Type."),
    416: _("Requested Range Not Satisfiable."),
    417: _("Expectation Failed."),
    418: _("I'm a teapot."),  # see RFC 2324
    422: _("Unprocessable Entity."),
    423: _("Locked."),
    424: _("Failed Dependency."),
    426: _("Upgrade Required."),
    428: _("Precondition Required."),  # see RFC 6585
    429: _("Too Many Requests."),
    431: _("Request Header Fields Too Large."),
    449: _("Retry With."),  # proprietary MS extension

    500: _("Internal Server Error."),
    501: _("Not Implemented."),
    502: _("Bad Gateway."),
    503: _("Service Unavailable."),
    504: _("Gateway Timeout."),
    505: _("HTTP Version Not Supported."),
    507: _("Insufficient Storage."),
    510: _("Not Extended.")
}

HTTP_100_CONTINUE = {
}
HTTP_101_SWITCHING_PROTOCOLS = {
}
HTTP_200_OK = {
}
HTTP_201_CREATED = {
}
HTTP_202_ACCEPTED = {
}
HTTP_203_NON_AUTHORITATIVE_INFORMATION = {
}
HTTP_204_NO_CONTENT = {
}
HTTP_205_RESET_CONTENT = {
}
HTTP_206_PARTIAL_CONTENT = {
}
HTTP_300_MULTIPLE_CHOICES = {
}
HTTP_301_MOVED_PERMANENTLY = {
}
HTTP_302_FOUND = {
}
HTTP_303_SEE_OTHER = {
}
HTTP_304_NOT_MODIFIED = {
}
HTTP_305_USE_PROXY = {
}
HTTP_306_RESERVED = {
}
HTTP_307_TEMPORARY_REDIRECT = {
}

HTTP_400_BAD_REQUEST = {
    400000: _("{}"),
    400001: _("Content-Type in request header is not 'application/json'!"),
    400002: _("Missing field in request!")
}

HTTP_401_UNAUTHORIZED = {
    401000: _("{}"),
    401001: _("Authentication Failed: Wrong email or password."),
    401002: _("Missing authorization JWT token."),
    401003: _("Invalid token.")
}

HTTP_403_FORBIDDEN = {
    403001: _("Access denied!"),
    403002: _("You do not have permission to perform this action."),
}

HTTP_404_NOT_FOUND = {
}
HTTP_405_METHOD_NOT_ALLOWED = {
}
HTTP_406_NOT_ACCEPTABLE = {
}
HTTP_407_PROXY_AUTHENTICATION_REQUIRED = {
}
HTTP_408_REQUEST_TIMEOUT = {
}
HTTP_409_CONFLICT = {
}
HTTP_410_GONE = {
}
HTTP_411_LENGTH_REQUIRED = {
}
HTTP_412_PRECONDITION_FAILED = {
}
HTTP_413_REQUEST_ENTITY_TOO_LARGE = {
}
HTTP_414_REQUEST_URI_TOO_LONG = {
}
HTTP_415_UNSUPPORTED_MEDIA_TYPE = {
    415001: _("File too large, max file upload {} Mb"),
}
HTTP_416_REQUESTED_RANGE_NOT_SATISFIABLE = {
}
HTTP_417_EXPECTATION_FAILED = {
}

HTTP_422_UNPROCESSABLE_ENTITY = {
    422001: _("Metadata: {0} - {1} already exists"),
    422002: _("Language: {0} already exists")
}

HTTP_428_PRECONDITION_REQUIRED = {
}
HTTP_429_TOO_MANY_REQUESTS = {
}
HTTP_431_REQUEST_HEADER_FIELDS_TOO_LARGE = {
}

HTTP_500_INTERNAL_SERVER_ERROR = {
    500001: _("Internal server error")
}

HTTP_501_NOT_IMPLEMENTED = {
}
HTTP_502_BAD_GATEWAY = {
}
HTTP_503_SERVICE_UNAVAILABLE = {
}
HTTP_504_GATEWAY_TIMEOUT = {
}
HTTP_505_HTTP_VERSION_NOT_SUPPORTED = {
}
HTTP_511_NETWORK_AUTHENTICATION_REQUIRED = {
}
