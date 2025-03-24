# AUTO GENERATED FILE - DO NOT EDIT

import typing  # noqa: F401
import numbers # noqa: F401
from typing_extensions import TypedDict, NotRequired, Literal # noqa: F401
from dash.development.base_component import Component, _explicitize_args
try:
    from dash.development.base_component import ComponentType # noqa: F401
except ImportError:
    ComponentType = typing.TypeVar("ComponentType", bound=Component)


class DialogBody(Component):
    """A DialogBody component.
Body of the dialog, optionally with a constrained container height which allows vertical scrolling of its content.

Keyword arguments:

- children (a list of or a singular dash component, string or number; optional):
    DialogBody contents.

- id (string; optional):
    The ID used to identify this component in Dash callbacks.

- className (string; optional):
    A space-delimited list of class names to pass along to a child
    element.

- useOverflowScrollContainer (boolean; optional):
    Enable scrolling for the container."""
    _children_props = []
    _base_nodes = ['children']
    _namespace = 'dash_blueprint_components'
    _type = 'DialogBody'

    @_explicitize_args
    def __init__(
        self,
        children: typing.Optional[typing.Union[str, int, float, ComponentType, typing.Sequence[typing.Union[str, int, float, ComponentType]]]] = None,
        id: typing.Optional[typing.Union[str, dict]] = None,
        className: typing.Optional[str] = None,
        useOverflowScrollContainer: typing.Optional[bool] = None,
        style: typing.Optional[typing.Any] = None,
        **kwargs
    ):
        self._prop_names = ['children', 'id', 'className', 'style', 'useOverflowScrollContainer']
        self._valid_wildcard_attributes =            []
        self.available_properties = ['children', 'id', 'className', 'style', 'useOverflowScrollContainer']
        self.available_wildcard_properties =            []
        _explicit_args = kwargs.pop('_explicit_args')
        _locals = locals()
        _locals.update(kwargs)  # For wildcard attrs and excess named props
        args = {k: _locals[k] for k in _explicit_args if k != 'children'}

        super(DialogBody, self).__init__(children=children, **args)
