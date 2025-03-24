# AUTO GENERATED FILE - DO NOT EDIT

from dash.development.base_component import Component, _explicitize_args


class NavbarHeading(Component):
    """A NavbarHeading component.
Heading of the navbar

Keyword arguments:

- children (a list of or a singular dash component, string or number; optional):
    Content of the NavbarHeading.

- id (string; optional):
    The ID used to identify this component in Dash callbacks.

- className (string; optional):
    A space-delimited list of class names to pass along to a child
    element.

- style (dict; optional):
    CSS properties to apply to the root element."""
    _children_props = []
    _base_nodes = ['children']
    _namespace = 'dash_blueprint_components'
    _type = 'NavbarHeading'
    @_explicitize_args
    def __init__(self, children=None, id=Component.UNDEFINED, className=Component.UNDEFINED, style=Component.UNDEFINED, **kwargs):
        self._prop_names = ['children', 'id', 'className', 'style']
        self._valid_wildcard_attributes =            []
        self.available_properties = ['children', 'id', 'className', 'style']
        self.available_wildcard_properties =            []
        _explicit_args = kwargs.pop('_explicit_args')
        _locals = locals()
        _locals.update(kwargs)  # For wildcard attrs and excess named props
        args = {k: _locals[k] for k in _explicit_args if k != 'children'}

        super(NavbarHeading, self).__init__(children=children, **args)
