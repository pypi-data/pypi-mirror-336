"""
----------------------------------------------------------------------------------------------------
Written by:
  - Yovany Dominico Girón (y.dominico.giron@elprat.cat)

for Ajuntament del Prat de Llobregat
----------------------------------------------------------------------------------------------------

----------------------------------------------------------------------------------------------------
"""
from pydantic import ConfigDict
from pydantic.fields import ModelField


class ConStr(str):
    """Custom string type"""

    min_length = 0
    max_length = 0

    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, value: str, field: ModelField, config: ConfigDict):  # pylint: disable=unused-argument
        """Validate the string"""

        if not isinstance(value, str):
            raise ValueError('This value is only str')

        if not cls.min_length <= len(value) <= cls.max_length:
            raise ValueError(
                f"This value length {cls.min_length} ~ {cls.max_length}")

        return value
