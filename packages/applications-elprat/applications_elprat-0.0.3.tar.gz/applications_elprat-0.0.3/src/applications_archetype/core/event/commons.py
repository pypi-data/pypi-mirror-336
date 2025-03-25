"""
----------------------------------------------------------------------------------------------------
Written by Yovany Dominico Girón (y.dominico.giron@elprat.cat) for Ajuntament del Prat de Llobregat
----------------------------------------------------------------------------------------------------

----------------------------------------------------------------------------------------------------
"""
import inspect

from abc import ABC, abstractmethod
from typing import Type, Dict, Union, Optional, NoReturn

from contextvars import ContextVar

import anyio

from pydantic import BaseModel

from nomenclators_archetype.domain.exceptions import (InvalidEventTypeException, InvalidParameterTypeException,
                                                      EmptyContextException, ParameterCountException, RequiredParameterException)


class BaseEvent(ABC):
    """Base Event Protocol"""

    @abstractmethod
    async def handle(self, param: Union[Type[BaseModel], None] = None) -> None:
        """Handle the event"""


class EventHandlerValidator:
    """Event handler validator."""

    EVENT_PARAMETER_COUNT = 2

    async def validate(self, event: Type[BaseEvent], param: BaseModel = None) -> Optional[NoReturn]:
        """Validate the event and parameter."""

        if not issubclass(event, BaseEvent):
            raise InvalidEventTypeException

        if param and not isinstance(param, BaseModel):
            raise InvalidParameterTypeException

        signature = inspect.signature(event.handle)
        func_parameters = signature.parameters
        if len(func_parameters) != self.EVENT_PARAMETER_COUNT:
            raise ParameterCountException

        base_parameter = func_parameters.get("param")
        if base_parameter.default is not None and not param:
            raise RequiredParameterException(
                cls_name=base_parameter.__class__.__name__,
            )


class EventHandler:
    """Event handler."""

    def __init__(self, validator: EventHandlerValidator):
        self.events: Dict[BaseEvent, Union[BaseModel, None]] = {}
        self.validator = validator

    async def store(self, event: BaseEvent, param: BaseModel = None) -> None:
        """Store the event and parameter."""

        await self.validator.validate(event=type(event), param=param)
        self.events[event] = param

    async def publish(self) -> None:
        """Publish the events."""

        await self._run()

        self.events.clear()

    async def _run(self) -> None:
        """Run the events."""

        event: BaseEvent
        async with anyio.create_task_group() as task_group:
            for event, parameter in self.events.items():
                task_group.start_soon(event.handle, parameter)


_handler_context: ContextVar[Union["EventHandler", None]] = ContextVar(
    "_handler_context", default=None)


class EventHandlerMeta(type):
    """Event handler metaclass."""

    async def store(self, event: BaseEvent, param: BaseModel = None) -> None:  # pylint: disable=bad-mcs-method-argument
        """Store the event and parameter."""

        handler = self._get_event_handler()  # pylint: disable=no-value-for-parameter
        await handler.store(event=event, param=param)

    async def publish(self) -> None:  # pylint: disable=bad-mcs-method-argument
        """Publish the events."""

        handler = self._get_event_handler()  # pylint: disable=no-value-for-parameter
        await handler.publish()

    def _get_event_handler(self) -> Union[EventHandler, NoReturn]:  # pylint: disable=bad-mcs-method-argument
        """Get the event handler."""

        try:
            return _handler_context.get()
        except LookupError as exc:
            raise EmptyContextException from exc


class EventHandlerDelegator(metaclass=EventHandlerMeta):
    """Event handler delegator."""

    def __init__(self):
        self.token = None

    def __enter__(self):
        validator = EventHandlerValidator()
        self.token = _handler_context.set(EventHandler(validator=validator))
        return type(self)

    def __exit__(self, exc_type, exc_value, traceback):
        _handler_context.reset(self.token)


event_handler: Type[EventHandlerDelegator] = EventHandlerDelegator


class EventDispatcher:
    """Event dispatcher decorator."""

    def __call__(self, func):
        async def wrapper(*args, **kwargs):
            try:
                res = await func(*args, **kwargs)
            except Exception as ex:
                raise ex from None

            await event_handler.publish()
            return res

        return wrapper
