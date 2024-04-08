from __future__ import annotations

from functools import partial

from pydantic import BaseModel

from fastapi_utils.camelcase import snake2camel

try:
    from pydantic import ConfigDict

    class APIModel(BaseModel):
        """
        Intended for use as a base class for externally-facing models.

        Any models that inherit from this class will:
        * accept fields using snake_case or camelCase keys
        * use camelCase keys in the generated OpenAPI spec
        * have orm_mode on by default
            * Because of this, FastAPI will automatically attempt to parse returned orm instances into the model
        """

        model_config = ConfigDict(
            alias_generator=partial(snake2camel, start_lower=True),
            populate_by_name=True,
            from_attributes=True,
        )
except ImportError:
    from pydantic import BaseConfig

    class APIModel(BaseModel):
        """
        Intended for use as a base class for externally-facing models.

        Any models that inherit from this class will:
        * accept fields using snake_case or camelCase keys
        * use camelCase keys in the generated OpenAPI spec
        * have orm_mode on by default
            * Because of this, FastAPI will automatically attempt to parse returned orm instances into the model
        """

        class Config(BaseConfig):
            orm_mode = True
            allow_population_by_field_name = True
            alias_generator = partial(snake2camel, start_lower=True)


class APIMessage(APIModel):
    """
    A lightweight utility class intended for use with simple message-returning endpoints.
    """

    detail: str
