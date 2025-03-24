# AUTO GENERATED FILE - DO NOT EDIT

import typing  # noqa: F401
import numbers # noqa: F401
from typing_extensions import TypedDict, NotRequired, Literal # noqa: F401
from dash.development.base_component import Component, _explicitize_args
try:
    from dash.development.base_component import ComponentType # noqa: F401
except ImportError:
    ComponentType = typing.TypeVar("ComponentType", bound=Component)


class Tab(Component):
    """A Tab component.
Tab is a minimal wrapper with no functionality of its own—it is managed entirely by its parent Tabs wrapper.

Keyword arguments:

- id (string; optional):
    The ID used to identify this component in Dash callbacks.

- className (string; optional):
    A space-delimited list of class names to pass along to a child
    element.

- disabled (boolean; optional):
    Whether the tab is disabled.

- icon (string; optional):
    Name of a Blueprint UI icon to render before the children.

- panel (a list of or a singular dash component, string or number; optional):
    Panel content, rendered by the parent Tabs when this tab is
    active. If omitted,  no panel will be rendered for this tab.

- panelClassName (string; optional):
    Space-delimited string of class names applied to tab panel
    container.

- title (a list of or a singular dash component, string or number; optional):
    Content of tab title, rendered in a list above the active panel."""
    _children_props = ['panel', 'title']
    _base_nodes = ['panel', 'title', 'children']
    _namespace = 'dash_blueprint_components'
    _type = 'Tab'

    @_explicitize_args
    def __init__(
        self,
        id: typing.Optional[typing.Union[str, dict]] = None,
        className: typing.Optional[str] = None,
        disabled: typing.Optional[bool] = None,
        icon: typing.Optional[str] = None,
        panel: typing.Optional[typing.Union[str, int, float, ComponentType, typing.Sequence[typing.Union[str, int, float, ComponentType]]]] = None,
        panelClassName: typing.Optional[str] = None,
        title: typing.Optional[typing.Union[str, int, float, ComponentType, typing.Sequence[typing.Union[str, int, float, ComponentType]]]] = None,
        **kwargs
    ):
        self._prop_names = ['id', 'className', 'disabled', 'icon', 'panel', 'panelClassName', 'title']
        self._valid_wildcard_attributes =            []
        self.available_properties = ['id', 'className', 'disabled', 'icon', 'panel', 'panelClassName', 'title']
        self.available_wildcard_properties =            []
        _explicit_args = kwargs.pop('_explicit_args')
        _locals = locals()
        _locals.update(kwargs)  # For wildcard attrs and excess named props
        args = {k: _locals[k] for k in _explicit_args}

        super(Tab, self).__init__(**args)
