# AUTO GENERATED FILE - DO NOT EDIT

import typing  # noqa: F401
import numbers # noqa: F401
from typing_extensions import TypedDict, NotRequired, Literal # noqa: F401
from dash.development.base_component import Component, _explicitize_args
try:
    from dash.development.base_component import ComponentType # noqa: F401
except ImportError:
    ComponentType = typing.TypeVar("ComponentType", bound=Component)


class Radio(Component):
    """A Radio component.
A radio button typically represents a single option in a mutually exclusive list

Keyword arguments:

- children (a list of or a singular dash component, string or number; optional):
    JSX label for the control.

- id (string; optional):
    The ID used to identify this component in Dash callbacks.

- alignIndicator (string; optional):
    Alignment of the indicator within container.

- checked (boolean; optional):
    Whether the control is checked.

- className (string; optional):
    A space-delimited list of class names to pass along to a child
    element.

- defaultChecked (boolean; optional):
    Whether the control is initially checked (uncontrolled mode).

- disabled (boolean; optional):
    Whether the control is non-interactive.

- inline (boolean; optional):
    Whether the control should appear as an inline element.

- label (string; optional):
    Use children or labelElement to supply JSX content. This prop
    actually  supports JSX elements, but TypeScript will throw an
    error because  HTMLAttributes only allows strings.

- labelElement (a list of or a singular dash component, string or number; optional):
    JSX Element label for the control. This prop is a workaround for
    TypeScript  consumers as the type definition for label only
    accepts strings.  JavaScript consumers can provide a JSX element
    directly to label.

- large (boolean; optional):
    Whether this control should use large styles.

- tagName (string; optional):
    Name of the HTML tag that wraps the checkbox. By default a <label>
    is used,  which effectively enlarges the click target to include
    all of its children.  Supply a different tag name if this behavior
    is undesirable or you're listening  to click events from a parent
    element (as the label can register duplicate clicks).

- value (string; optional):
    Value of the radio."""
    _children_props = ['labelElement']
    _base_nodes = ['labelElement', 'children']
    _namespace = 'dash_blueprint_components'
    _type = 'Radio'

    @_explicitize_args
    def __init__(
        self,
        children: typing.Optional[typing.Union[str, int, float, ComponentType, typing.Sequence[typing.Union[str, int, float, ComponentType]]]] = None,
        id: typing.Optional[typing.Union[str, dict]] = None,
        alignIndicator: typing.Optional[str] = None,
        checked: typing.Optional[bool] = None,
        className: typing.Optional[str] = None,
        defaultChecked: typing.Optional[bool] = None,
        disabled: typing.Optional[bool] = None,
        inline: typing.Optional[bool] = None,
        label: typing.Optional[str] = None,
        labelElement: typing.Optional[typing.Union[str, int, float, ComponentType, typing.Sequence[typing.Union[str, int, float, ComponentType]]]] = None,
        large: typing.Optional[bool] = None,
        style: typing.Optional[typing.Any] = None,
        tagName: typing.Optional[str] = None,
        value: typing.Optional[str] = None,
        **kwargs
    ):
        self._prop_names = ['children', 'id', 'alignIndicator', 'checked', 'className', 'defaultChecked', 'disabled', 'inline', 'label', 'labelElement', 'large', 'style', 'tagName', 'value']
        self._valid_wildcard_attributes =            []
        self.available_properties = ['children', 'id', 'alignIndicator', 'checked', 'className', 'defaultChecked', 'disabled', 'inline', 'label', 'labelElement', 'large', 'style', 'tagName', 'value']
        self.available_wildcard_properties =            []
        _explicit_args = kwargs.pop('_explicit_args')
        _locals = locals()
        _locals.update(kwargs)  # For wildcard attrs and excess named props
        args = {k: _locals[k] for k in _explicit_args if k != 'children'}

        super(Radio, self).__init__(children=children, **args)
