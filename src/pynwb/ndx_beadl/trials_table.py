from pynwb import register_class
from pynwb.core import DynamicTable
from pynwb.epoch import TimeIntervals
from hdmf.utils import docval, get_docval, getargs, popargs, call_docval_func, AllowPositional


@register_class('TrialsTable', 'ndx-beadl')
class TrialsTable(TimeIntervals):
    """A table to hold trials data."""

    __columns__ = (
        {
            'name': 'states',
            'description': ('The states'),
            'index': True,
            'table': True,
            'required': False
        },
        {
            'name': 'events',
            'description': ('The events.'),
            'index': True,
            'table': True,
            'required': False
        },
    )

    @docval(
        *get_docval(DynamicTable.__init__, 'id', 'columns', 'colnames'),
        {
            'name': 'description',
            'type': str,
            'doc': 'A description of what is in this table.',
            'default': 'Trial data',
        },
        {
            'name': 'states_table',
            'type': 'StatesTable',
            'doc': ('The states table.'),
            'default': None,
        },
        {
            'name': 'events_table',
            'type': 'EventsTable',
            'doc': ('The events table.'),
            'default': None,
        },
        allow_positional=AllowPositional.ERROR,
    )
    def __init__(self, **kwargs):
        kwargs['name'] = 'trials'
        # store the table references as instance vars in case the DTR column does not exist yet
        # and a row is added later which results in the DTR column being created.
        # if the DTR column is not added and no rows are added, then these table references
        # are not used.
        self._states_table = popargs('states_table', kwargs)
        self._events_table = popargs('events_table', kwargs)
        call_docval_func(super().__init__, kwargs)
        self._set_dtr_ref()

    @docval(
        {
            'name': 'states',
            'type': 'array_data',
            'doc': ('The states.'),
        },
        {
            'name': 'events',
            'type': 'array_data',
            'doc': ('The events.'),
        },
        allow_extra=True,
        allow_positional=AllowPositional.ERROR,
    )
    def add_row(self, **kwargs):
        """Add a trial to this table."""
        super().add_row(**kwargs)
        self._set_dtr_ref()

    add_trial = add_row  # alias for add_row

    def _set_dtr_ref(self):
        # set the DynamicTableRegion table reference if the table reference has been provided and the
        # column already exists
        if self._states_table is not None and self.states is not None and self.states.table is None:
            self.states.table = self._states_table

        if self._events_table is not None and self.events is not None and self.events.table is None:
            self.events.table = self._events_table


@register_class('StatesTable', 'ndx-beadl')
class StatesTable(TimeIntervals):
    """A table to hold states data."""

    __columns__ = (
        {
            'name': 'type',
            'description': ('The state type'),
            'table': True,
            'required': True
        },
    )

    @docval(
        *get_docval(DynamicTable.__init__, 'id', 'columns', 'colnames'),
        {
            'name': 'description',
            'type': str,
            'doc': 'A description of what is in this table.',
            'default': 'State data',
        },
        {
            'name': 'state_types_table',
            'type': 'StateTypesTable',
            'doc': ('The states table.'),
        },
        allow_positional=AllowPositional.ERROR,
    )
    def __init__(self, **kwargs):
        kwargs['name'] = 'states'
        state_types_table = popargs('state_types_table', kwargs)
        call_docval_func(super().__init__, kwargs)
        if self.type is not None and self.type.table is None:
            self.type.table = state_types_table

    @docval(
        {
            'name': 'type',
            'type': int,
            'doc': ('The state type for this state.'),
        },
        allow_extra=True,
        allow_positional=AllowPositional.ERROR,
    )
    def add_row(self, **kwargs):
        """Add a state to this table."""
        super().add_row(**kwargs)

    add_state = add_row  # alias for add_row


@register_class('EventsTable', 'ndx-beadl')
class EventsTable(DynamicTable):
    """A table to hold events data."""

    __columns__ = (
        {
            'name': 'type',
            'description': ('The event type'),
            'table': True,
            'required': True
        },
        {
            'name': 'timestamp',
            'description': ('The event timestamp'),
            'required': True
        },
    )

    @docval(
        *get_docval(DynamicTable.__init__, 'id', 'columns', 'colnames'),
        {
            'name': 'description',
            'type': str,
            'doc': 'A description of what is in this table.',
            'default': 'Event data',
        },
        {
            'name': 'event_types_table',
            'type': 'EventTypesTable',
            'doc': ('The events table.'),
            'default': None,
        },
        allow_positional=AllowPositional.ERROR,
    )
    def __init__(self, **kwargs):
        kwargs['name'] = 'events'
        event_types_table = popargs('event_types_table', kwargs)
        call_docval_func(super().__init__, kwargs)
        if event_types_table is not None and self.type is not None and self.type.table is None:
            self.type.table = event_types_table

    @docval(
        {
            'name': 'type',
            'type': int,
            'doc': ('The event type.'),
        },
        {
            'name': 'timestamp',
            'type': float,
            'doc': ('The event timestamp.'),
        },
        allow_extra=True,
        allow_positional=AllowPositional.ERROR,
    )
    def add_row(self, **kwargs):
        """Add an event to this table."""
        super().add_row(**kwargs)

    add_event = add_row  # alias for add_row
