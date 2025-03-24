# AUTO GENERATED FILE - DO NOT EDIT

import typing  # noqa: F401
import numbers # noqa: F401
from typing_extensions import TypedDict, NotRequired, Literal # noqa: F401
from dash.development.base_component import Component, _explicitize_args
try:
    from dash.development.base_component import ComponentType # noqa: F401
except ImportError:
    ComponentType = typing.TypeVar("ComponentType", bound=Component)


class Breadcrumb(Component):
    """A Breadcrumb component.
Breadcrumbs identify the path to the current resource in an application.

Keyword arguments:

- id (string; optional):
    The ID used to identify this component in Dash callbacks.

- alwaysRenderOverflow (boolean; optional):
    Whether to display all the collapsed items or just the last one.

- className (string; optional):
    A space-delimited list of class names to pass along to a child
    element.

- collapseFrom (string; optional):
    Which direction the breadcrumbs should collapse from: start or
    end.

- items (list; optional):
    All breadcrumbs to display. Breadcrumbs that do not fit  in the
    container will be rendered in an overflow menu instead.

- minVisibleItems (number; optional):
    The minimum number of visible breadcrumbs that should never
    collapse into the overflow menu, regardless of DOM dimensions."""
    _children_props = []
    _base_nodes = ['children']
    _namespace = 'dash_blueprint_components'
    _type = 'Breadcrumb'

    @_explicitize_args
    def __init__(
        self,
        id: typing.Optional[typing.Union[str, dict]] = None,
        alwaysRenderOverflow: typing.Optional[bool] = None,
        className: typing.Optional[str] = None,
        collapseFrom: typing.Optional[str] = None,
        items: typing.Optional[typing.Sequence] = None,
        minVisibleItems: typing.Optional[typing.Union[int, float, numbers.Number]] = None,
        style: typing.Optional[typing.Any] = None,
        **kwargs
    ):
        self._prop_names = ['id', 'alwaysRenderOverflow', 'className', 'collapseFrom', 'items', 'minVisibleItems', 'style']
        self._valid_wildcard_attributes =            []
        self.available_properties = ['id', 'alwaysRenderOverflow', 'className', 'collapseFrom', 'items', 'minVisibleItems', 'style']
        self.available_wildcard_properties =            []
        _explicit_args = kwargs.pop('_explicit_args')
        _locals = locals()
        _locals.update(kwargs)  # For wildcard attrs and excess named props
        args = {k: _locals[k] for k in _explicit_args}

        super(Breadcrumb, self).__init__(**args)
