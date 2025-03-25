"""
----------------------------------------------------------------------------------------------------
Written by:
  - Yovany Dominico Girón (y.dominico.giron@elprat.cat)

for Ajuntament del Prat de Llobregat
----------------------------------------------------------------------------------------------------

----------------------------------------------------------------------------------------------------
"""
from fastapi import Request

from starlette.responses import Response
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint

from applications_archetype.core.event.commons import event_handler


class EventMiddleware(BaseHTTPMiddleware):
    """Event handler middleware."""

    async def dispatch(self, request: Request, call_next: RequestResponseEndpoint) -> Response:
        try:
            with event_handler():
                res = await call_next(request)
        except Exception as ex:
            raise ex from None

        return res
