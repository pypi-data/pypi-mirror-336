# AUTO GENERATED FILE - DO NOT EDIT

import typing  # noqa: F401
import numbers # noqa: F401
from typing_extensions import TypedDict, NotRequired, Literal # noqa: F401
from dash.development.base_component import Component, _explicitize_args
try:
    from dash.development.base_component import ComponentType # noqa: F401
except ImportError:
    ComponentType = typing.TypeVar("ComponentType", bound=Component)


class DateInput(Component):
    """A DateInput component.
The DateInput component is an InputGroup that shows a DatePicker inside a Popover on focus. 
It optionally shows a TimezoneSelect on the right side of the InputGroup, allowing the user 
to change the timezone of the selected date.

Keyword arguments:

- id (string; optional):
    The ID used to identify this component in Dash callbacks.

- canClearSelection (boolean; optional):
    Allows the user to clear the selection by clicking the currently
    selected day. Passed to DatePicker component.

- className (string; optional):
    A space-delimited list of class names to pass along to a child
    element.

- clearButtonText (string; optional):
    Text for the reset button in the date picker action bar. Passed to
    DatePicker component.

- closeOnSelection (string; optional):
    Whether the calendar popover should close when a date is selected.

- date (string; optional):
    An ISO string representing the selected time.

- dateFnsFormat (string; optional):
    date-fns format string used to format & parse date strings.

- defaultTimezone (string; optional):
    The default timezone selected. Defaults to the user local
    timezone.

- defaultValue (string; optional):
    The default date to be used in the component when uncontrolled,
    represented as an ISO string.

- disableTimezoneSelect (boolean; optional):
    Whether to disable the timezone select.

- disabled (boolean; optional):
    Whether the date input is non-interactive.

- fill (boolean; optional):
    Whether the component should take up the full width of its
    container.

- footerElement (a list of or a singular dash component, string or number; optional):
    An additional element to show below the date picker.

- highlightCurrentDay (boolean; optional):
    Whether the current day should be highlighted in the calendar.

- initialMonth (string; optional):
    The initial month the calendar displays.

- invalidDateMessage (string; optional):
    The error message to display when the date selected is invalid.

- locale (string; optional):
    date-fns Locale object or locale code string ((ISO 639-1 +
    optional country code) which  will be used to localize the date
    picker. If you provide a locale code string and receive  a loading
    error, please make sure it is included in the list of date-fns'.

- maxDate (string; optional):
    The latest date the user can select.

- minDate (string; optional):
    The earliest date the user can select.

- outOfRangeMessage (string; optional):
    The error message to display when the date selected is out of
    range.

- placeholder (string; optional):
    Placeholder text to display in empty input fields. Recommended
    practice is to indicate the expected date format.

- reverseMonthAndYearMenus (boolean; optional):
    If True, the month menu will appear to the left of the year menu.
    Otherwise, the month menu will apear to  the right of the year
    menu.

- rightElement (a list of or a singular dash component, string or number; optional):
    Element to render on right side of input.

- selectedShortcutIndex (number; optional):
    The currently selected shortcut. If this prop is provided, the
    component acts in a controlled manner.

- shortcuts (boolean; optional):
    Whether shortcuts to quickly select a date are displayed or not.
    If True, preset shortcuts will be displayed. If False,  no
    shortcuts will be displayed.

- showActionsBar (boolean; optional):
    Whether the bottom bar displaying \"Today\" and \"Clear\" buttons
    should be shown.

- showTimeArrowButtons (boolean; optional):
    Whether arrows for selecting the time should be shown.

- showTimezoneSelect (boolean; optional):
    Whether to show the timezone select dropdown on the right side of
    the input. If timePrecision is undefined, this will always be
    False.

- timePrecision (string; optional):
    The precision of time selection that accompanies the calendar.
    Passing a TimePrecision value shows a TimePicker below the
    calendar. Time is preserved across date changes. Either 'minute',
    'second', 'millisecond'.

- todayButtonText (string; optional):
    Text for the today button in the action bar.

- useAmPm (boolean; optional):
    Whether the time should be displayed as AM/PM."""
    _children_props = ['footerElement', 'rightElement']
    _base_nodes = ['footerElement', 'rightElement', 'children']
    _namespace = 'dash_blueprint_components'
    _type = 'DateInput'

    @_explicitize_args
    def __init__(
        self,
        id: typing.Optional[typing.Union[str, dict]] = None,
        canClearSelection: typing.Optional[bool] = None,
        className: typing.Optional[str] = None,
        clearButtonText: typing.Optional[str] = None,
        closeOnSelection: typing.Optional[str] = None,
        date: typing.Optional[str] = None,
        dateFnsFormat: typing.Optional[str] = None,
        defaultTimezone: typing.Optional[str] = None,
        defaultValue: typing.Optional[str] = None,
        disabled: typing.Optional[bool] = None,
        disableTimezoneSelect: typing.Optional[bool] = None,
        fill: typing.Optional[bool] = None,
        footerElement: typing.Optional[typing.Union[str, int, float, ComponentType, typing.Sequence[typing.Union[str, int, float, ComponentType]]]] = None,
        highlightCurrentDay: typing.Optional[bool] = None,
        initialMonth: typing.Optional[str] = None,
        invalidDateMessage: typing.Optional[str] = None,
        locale: typing.Optional[str] = None,
        maxDate: typing.Optional[str] = None,
        minDate: typing.Optional[str] = None,
        outOfRangeMessage: typing.Optional[str] = None,
        placeholder: typing.Optional[str] = None,
        reverseMonthAndYearMenus: typing.Optional[bool] = None,
        rightElement: typing.Optional[typing.Union[str, int, float, ComponentType, typing.Sequence[typing.Union[str, int, float, ComponentType]]]] = None,
        selectedShortcutIndex: typing.Optional[typing.Union[int, float, numbers.Number]] = None,
        shortcuts: typing.Optional[bool] = None,
        showActionsBar: typing.Optional[bool] = None,
        showTimezoneSelect: typing.Optional[bool] = None,
        showTimeArrowButtons: typing.Optional[bool] = None,
        style: typing.Optional[typing.Any] = None,
        timePrecision: typing.Optional[str] = None,
        todayButtonText: typing.Optional[str] = None,
        useAmPm: typing.Optional[bool] = None,
        **kwargs
    ):
        self._prop_names = ['id', 'canClearSelection', 'className', 'clearButtonText', 'closeOnSelection', 'date', 'dateFnsFormat', 'defaultTimezone', 'defaultValue', 'disableTimezoneSelect', 'disabled', 'fill', 'footerElement', 'highlightCurrentDay', 'initialMonth', 'invalidDateMessage', 'locale', 'maxDate', 'minDate', 'outOfRangeMessage', 'placeholder', 'reverseMonthAndYearMenus', 'rightElement', 'selectedShortcutIndex', 'shortcuts', 'showActionsBar', 'showTimeArrowButtons', 'showTimezoneSelect', 'style', 'timePrecision', 'todayButtonText', 'useAmPm']
        self._valid_wildcard_attributes =            []
        self.available_properties = ['id', 'canClearSelection', 'className', 'clearButtonText', 'closeOnSelection', 'date', 'dateFnsFormat', 'defaultTimezone', 'defaultValue', 'disableTimezoneSelect', 'disabled', 'fill', 'footerElement', 'highlightCurrentDay', 'initialMonth', 'invalidDateMessage', 'locale', 'maxDate', 'minDate', 'outOfRangeMessage', 'placeholder', 'reverseMonthAndYearMenus', 'rightElement', 'selectedShortcutIndex', 'shortcuts', 'showActionsBar', 'showTimeArrowButtons', 'showTimezoneSelect', 'style', 'timePrecision', 'todayButtonText', 'useAmPm']
        self.available_wildcard_properties =            []
        _explicit_args = kwargs.pop('_explicit_args')
        _locals = locals()
        _locals.update(kwargs)  # For wildcard attrs and excess named props
        args = {k: _locals[k] for k in _explicit_args}

        super(DateInput, self).__init__(**args)
