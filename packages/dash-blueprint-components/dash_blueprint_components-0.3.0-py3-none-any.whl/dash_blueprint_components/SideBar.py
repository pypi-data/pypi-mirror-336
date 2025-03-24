# AUTO GENERATED FILE - DO NOT EDIT

import typing  # noqa: F401
import numbers # noqa: F401
from typing_extensions import TypedDict, NotRequired, Literal # noqa: F401
from dash.development.base_component import Component, _explicitize_args
try:
    from dash.development.base_component import ComponentType # noqa: F401
except ImportError:
    ComponentType = typing.TypeVar("ComponentType", bound=Component)


class SideBar(Component):
    """A SideBar component.
Component for creating interactive Sidebars

Keyword arguments:

- id (string; optional):
    The ID used to identify this component in Dash callbacks.

- className (string; optional):
    A space-delimited list of class names to pass along to a child
    element.

- initialRoute (string; optional):
    initial route.

- items (list; optional):
    items to be displayed in the menu.

- route (string; optional):
    current selected route."""
    _children_props = []
    _base_nodes = ['children']
    _namespace = 'dash_blueprint_components'
    _type = 'SideBar'

    @_explicitize_args
    def __init__(
        self,
        id: typing.Optional[typing.Union[str, dict]] = None,
        className: typing.Optional[str] = None,
        items: typing.Optional[typing.Sequence] = None,
        route: typing.Optional[str] = None,
        initialRoute: typing.Optional[str] = None,
        style: typing.Optional[typing.Any] = None,
        **kwargs
    ):
        self._prop_names = ['id', 'className', 'initialRoute', 'items', 'route', 'style']
        self._valid_wildcard_attributes =            []
        self.available_properties = ['id', 'className', 'initialRoute', 'items', 'route', 'style']
        self.available_wildcard_properties =            []
        _explicit_args = kwargs.pop('_explicit_args')
        _locals = locals()
        _locals.update(kwargs)  # For wildcard attrs and excess named props
        args = {k: _locals[k] for k in _explicit_args}

        super(SideBar, self).__init__(**args)
