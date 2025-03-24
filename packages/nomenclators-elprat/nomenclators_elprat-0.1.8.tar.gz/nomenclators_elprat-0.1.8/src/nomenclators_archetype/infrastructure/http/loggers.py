"""
----------------------------------------------------------------------------------------------------
Written by:
  - Yovany Dominico Girón(y.dominico.giron@elprat.cat)

for Ajuntament del Prat de Llobregat
----------------------------------------------------------------------------------------------------

----------------------------------------------------------------------------------------------------
"""
import os
import sys
import uuid
import time
import socket
import logging

from types import SimpleNamespace
from datetime import datetime, timezone

from pythonjsonlogger.json import JsonFormatter

from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint

from nomenclators_archetype.domain.loggers import LOGGER_LEVEL, LoggerBuilder
from nomenclators_archetype.infrastructure.http.auths import APPLICATION_ID, get_user_from_jwt


JSON_LOGGER_ENV_NAME = "JSON_LOGGER_NAME"
JSON_LOGGER_NAME_DEFAULT = "logger_console_json"
JSON_LOGGER_NAME = os.getenv(JSON_LOGGER_ENV_NAME, JSON_LOGGER_NAME_DEFAULT)


class LoggerJSONBuilder(LoggerBuilder):
    """Logger JSON builder class"""

    def get_handler(self):
        """Gets the handler of the logger"""
        return logging.StreamHandler(sys.stdout)

    def get_formatter(self):
        """Gets the formatter of the logger"""
        return JsonFormatter(
            "%(timestamp)s %(client_request_id)s %(server_request_id)s %(application_id)s "
            "%(request_time)s %(entry_time)s %(user)s %(client_session_id)s "
            "%(client_ip)s %(server_ip)s %(server_port)s %(service)s %(http_method)s "
            "%(module)s %(response_code)s %(response_time)s"
        )


class LoggerJSONMiddleware(BaseHTTPMiddleware):
    """Logger handler middleware."""

    def __init__(self, app, dispatch=None):
        super().__init__(app, dispatch)
        self.logger = LoggerJSONBuilder(
            name=JSON_LOGGER_NAME, level=LOGGER_LEVEL).build()

    async def dispatch(self, request: Request, call_next: RequestResponseEndpoint) -> Response:
        """Logger middlewares for the requests router"""
        start_time = time.time()
        request_time = datetime.now(timezone.utc).isoformat()

        server_request_id = str(uuid.uuid4())
        client_request_id = request.headers.get(
            "X-Request-ID", None) if request.headers else None

        client_session_id = request.headers.get(
            "Authorization", None) if request.headers else None
        user = get_user_from_jwt(
            client_session_id) if client_session_id else None

        client_ip = request.client.host if request.client else None
        server_ip = request.base_url.hostname if request.base_url else socket.gethostbyname(
            socket.gethostname())
        server_port = request.base_url.port if request.base_url else None
        service = request.url.path
        http_method = request.method

        request.state.trace_info = getattr(request.state, "trace_info", {})

        response = await call_next(request)

        response_code = response.status_code

        trace_info = getattr(request.state, "trace_info", {})
        if isinstance(trace_info, dict):
            trace_info = SimpleNamespace(**trace_info)

        response_time = round(time.time() - start_time, 4)
        response.headers["X-Process-Time"] = str(response_time)

        data_logger = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "client_request_id": client_request_id,
            "request_time": request_time,
            "server_request_id": server_request_id,
            "application_id": APPLICATION_ID,
            "user": user,
            "client_session_id": client_session_id,
            "client_ip": client_ip,
            "server_ip": server_ip,
            "server_port": server_port,
            "service": service,
            "http_method": http_method,
            "response_code": response_code,
            "response_module": getattr(trace_info, "module", None),
            "response_entity": getattr(trace_info, "entity", None),
            "response_id": getattr(trace_info, "identifier", None),
            "response_count": getattr(trace_info, "count", None),
            "response_page": getattr(trace_info, "page", None),
            "response_size": getattr(trace_info, "size", None),
            "response_time": response_time
        }

        self.logger.info(self._replace_dict_none_with_null(data_logger))
        return response

    def _replace_dict_none_with_null(self, data):
        """Replaces None values with the string 'null' in a dictionary"""

        if isinstance(data, dict):
            return {key: self._replace_dict_none_with_null(value) for key, value in data.items()}
        elif isinstance(data, list):
            return [self._replace_dict_none_with_null(item) for item in data]
        elif data is None:
            return "null"
        return data
