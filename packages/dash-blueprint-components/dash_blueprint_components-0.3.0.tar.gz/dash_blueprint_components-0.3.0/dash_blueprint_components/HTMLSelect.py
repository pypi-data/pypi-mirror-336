# AUTO GENERATED FILE - DO NOT EDIT

import typing  # noqa: F401
import numbers # noqa: F401
from typing_extensions import TypedDict, NotRequired, Literal # noqa: F401
from dash.development.base_component import Component, _explicitize_args
try:
    from dash.development.base_component import ComponentType # noqa: F401
except ImportError:
    ComponentType = typing.TypeVar("ComponentType", bound=Component)


class HTMLSelect(Component):
    """A HTMLSelect component.
Styling HTML <select> tags requires a wrapper element to customize the dropdown caret, 
so Blueprint provides a HTMLSelect component to streamline this process.

Keyword arguments:

- children (a list of or a singular dash component, string or number; optional):
    Radio elements. This prop is mutually exclusive with options.

- id (string; optional):
    The ID used to identify this component in Dash callbacks.

- disabled (boolean; optional):
    Whether this element is non-interactive.

- fill (boolean; optional):
    Whether this element should fill its container.

- iconName (string; default "double-caret-vertical"):
    Name of one of the supported icons for this component to display
    on the right side of the element.

- large (boolean; optional):
    Whether to use large styles.

- minimal (boolean; optional):
    Whether to use minimal styles.

- options (list; optional):
    Shorthand for supplying options: an array of { label?, value }
    objects. If no label is supplied,  value will be used as the
    label.

- value (number | string; optional):
    Controlled value of this component."""
    _children_props = []
    _base_nodes = ['children']
    _namespace = 'dash_blueprint_components'
    _type = 'HTMLSelect'

    @_explicitize_args
    def __init__(
        self,
        children: typing.Optional[typing.Union[str, int, float, ComponentType, typing.Sequence[typing.Union[str, int, float, ComponentType]]]] = None,
        id: typing.Optional[typing.Union[str, dict]] = None,
        disabled: typing.Optional[bool] = None,
        fill: typing.Optional[bool] = None,
        iconName: typing.Optional[str] = None,
        large: typing.Optional[bool] = None,
        minimal: typing.Optional[bool] = None,
        options: typing.Optional[typing.Sequence] = None,
        value: typing.Optional[typing.Union[typing.Union[int, float, numbers.Number], str]] = None,
        style: typing.Optional[typing.Any] = None,
        **kwargs
    ):
        self._prop_names = ['children', 'id', 'disabled', 'fill', 'iconName', 'large', 'minimal', 'options', 'style', 'value']
        self._valid_wildcard_attributes =            []
        self.available_properties = ['children', 'id', 'disabled', 'fill', 'iconName', 'large', 'minimal', 'options', 'style', 'value']
        self.available_wildcard_properties =            []
        _explicit_args = kwargs.pop('_explicit_args')
        _locals = locals()
        _locals.update(kwargs)  # For wildcard attrs and excess named props
        args = {k: _locals[k] for k in _explicit_args if k != 'children'}

        super(HTMLSelect, self).__init__(children=children, **args)
