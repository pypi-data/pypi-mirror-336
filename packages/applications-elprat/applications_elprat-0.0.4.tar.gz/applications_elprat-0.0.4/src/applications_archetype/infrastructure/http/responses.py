"""
----------------------------------------------------------------------------------------------------
Written by:
  - Yovany Dominico Girón (y.dominico.giron@elprat.cat)

for Ajuntament del Prat de Llobregat
----------------------------------------------------------------------------------------------------

----------------------------------------------------------------------------------------------------
"""
from typing import Any

from starlette.responses import JSONResponse
from sqlalchemy.ext.associationproxy import _AssociationList

try:
    import orjson  # type: ignore
except ImportError:  # pragma: nocover
    orjson = None  # type: ignore


def default(obj):
    """Default JSON serializer."""

    if isinstance(obj, _AssociationList):
        return list(obj)
    raise TypeError


class ORJSONResponse(JSONResponse):
    """ORJSON response class."""

    media_type = "application/json"

    def render(self, content: Any) -> bytes:
        assert orjson is not None, "orjson must be installed to use ORJSONResponse"
        return orjson.dumps(content, default=default)  # pylint: disable=no-member
