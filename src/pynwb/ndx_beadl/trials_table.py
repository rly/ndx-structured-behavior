from pynwb import register_class
from pynwb.file import LabMetaData
from pynwb.core import DynamicTable, NWBDataInterface
from pynwb.epoch import TimeIntervals
from hdmf.utils import docval, get_docval, getargs, popargs, AllowPositional
from ndx_beadl import BEADLTaskProgram
from .beadl_xml_parser import BeadlXMLParser
from .utils import loadmat
import itertools

@register_class('Task', 'ndx-beadl')
class Task(LabMetaData):
    __nwbfields__ = (
        {'name': 'task_program', 'child': True},
        {'name': 'task_schema', 'child': True},
        {'name': 'event_types', 'child': True},
        {'name': 'state_types', 'child': True},
        {'name': 'action_types', 'child': True},
        {'name': 'task_arguments', 'child': True}

    )
    @docval(
        {
            'name': 'task_program',
            'type': 'TaskProgram',
            'doc': 'A dataset to store a task program.',
        },
        {
            'name': 'task_schema',
            'type': 'TaskSchema',
            'doc': 'A dataset to store a task schema, e.g., an XSD file.',
        },
        {
            'name': 'event_types',
            'type': 'EventTypesTable',
            'doc': 'The table for event types populated by the task program',
        },
        {
            'name': 'state_types',
            'type': 'StateTypesTable',
            'doc': 'The table for state types populated by the task program',
        },
        {
            'name': 'action_types',
            'type': 'ActionTypesTable',
            'doc': 'The table for action types populated by the task program',
        },
        {
            'name': 'task_arguments',
            'type': 'TaskArgumentsTable',
            'doc': 'The table for task arguments populated by the task program',
        },
        allow_positional=AllowPositional.ERROR,
        )
    def __init__(self, **kwargs):
        kwargs['name'] = 'task'
        task_program = popargs('task_program', kwargs)
        task_schema = popargs('task_schema', kwargs)
        event_types = popargs('event_types', kwargs)
        state_types = popargs('state_types', kwargs)
        action_types = popargs('action_types', kwargs)
        task_arguments = popargs('task_arguments', kwargs)
        super().__init__(**kwargs)
        self.task_program = task_program
        self.task_schema = task_schema
        self.event_types = event_types
        self.state_types = state_types
        self.action_types = action_types
        self.task_arguments = task_arguments

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
        {
            'name': 'actions',
            'description': ('The actions.'),
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
            'doc': 'A table that holds the data from the trials.',
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
        {
            'name': 'actions_table',
            'type': 'ActionsTable',
            'doc': ('The actions table.'),
            'default': None,
        },
        allow_positional=AllowPositional.ERROR,
    )
    def __init__(self, **kwargs):
        kwargs['name'] = 'trials'
        self._states_table = popargs('states_table', kwargs)
        self._events_table = popargs('events_table', kwargs)
        self._action_table = popargs('actions_table', kwargs)
        super().__init__(**kwargs)
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
        {
            'name': 'actions',
            'type': 'array_data',
            'doc': ('The actions.'),
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

        if self._action_table is not None and self.actions is not None and self.actions.table is None:
            self.actions.table = self._action_table

    @docval(
        {
            'name': 'data_path',
            'type': str,
            'doc': 'The path to the matlab data file.'
        }
    )
    def populate_from_matlab(self, **kwargs):
        states_table = self._states_table
        events_table = self._events_table
        actions_table = self._action_table
        file_path = kwargs['data_path']

        matlab_file = loadmat(file_path)
        states_data = matlab_file['BeadlData']['States']
        events_data = matlab_file['BeadlData']['Events']
        args_data = matlab_file['BeadlData']['BeadlArguments']

        trial_paths = [i['TrialPath'] for i in states_data]

        # retrieve start and stop times for trial
        start_times = matlab_file['BeadlData']['SessionMetaData']['TrialStartOffset']
        stop_times=[]
        trial_length=[]
        for trial in trial_paths:
            end_time = trial[-1]['stateStartTime']
            stop_times.append(end_time)
            trial_length.append(len(trial))

        stop_times = [sum(value) for value in zip(start_times, stop_times)]

        states_index=[]
        states_index_ranges=[]
        for i in range(len(trial_length)):
            if i==0:
                states_index.append(trial_length[i])
                states_index_ranges.append(list(range(trial_length[i])))
            else:
                end=states_index[i-1]+trial_length[i]
                states_index.append(end)
                states_index_ranges.append(list(range(states_index[i-1], end)))


        #events vector index data
        trial_events_length =[]
        for trial in events_data:
            trial_events=trial['AllEvents']
            if type(trial_events)!= list:
                trial_events=[trial_events]
            trial_events_length.append(len(trial_events))

        events_index=[]
        events_index_ranges=[]
        for i in range(len(trial_events_length)):
            if i==0:
                events_index.append(trial_events_length[i])
                events_index_ranges.append(list(range(trial_events_length[i])))
            else:
                end=events_index[i-1]+trial_events_length[i]
                events_index.append(events_index[i-1]+trial_events_length[i])
                events_index_ranges.append(list(range(events_index[i-1], end)))

        #retrieve actions
        trial_actions_length =[]
        for trial in states_data:
            trial_actions=trial['StateOutputActions']
            if type(trial_actions)!= list:
                trial_actions=[trial_actions]
            trial_actions_length.append(len(trial_actions))

        action_index=[]
        action_index_ranges=[]
        for i in range(len(trial_actions_length)):
            if i==0:
                action_index.append(trial_actions_length[i])
                action_index_ranges.append(list(range(trial_actions_length[i])))
            else:
                end=action_index[i-1]+trial_actions_length[i]
                action_index.append(action_index[i-1]+trial_actions_length[i])
                action_index_ranges.append(list(range(action_index[i-1], end)))


        #populate trials_table
        for i in range(len(start_times)):
            self.add_trial(start_time=start_times[i], stop_time=stop_times[i], states=states_index_ranges[i], events=events_index_ranges[i], actions=action_index_ranges[i])

        #populate BeadlArguments as columns
        for arg in args_data:
            self.add_column(name=arg, description='Task Program Argument', data=args_data[arg])

        return self


@register_class('StatesTable', 'ndx-beadl')
class StatesTable(TimeIntervals):
    """A table to hold states data."""

    __columns__ = (
        {
            'name': 'state_type',
            'description': ('The state type'),
            'table': True,
            'required': True
        },
        {
            'name': 'start_time',
            'description': ('The state start time'),
            'required': True
        },
        {
            'name': 'stop_time',
            'description': ('The state stop time'),
            'required': True
        },
    )

    @docval(
        *get_docval(DynamicTable.__init__, 'id', 'columns', 'colnames'),
        {
            'name': 'description',
            'type': str,
            'doc': 'A table to hold states data.',
            'default': 'State data',
        },
        {
            'name': 'state_types_table',
            'type': 'StateTypesTable',
            'doc': ('The states table.'),
            'default': None
        },
        allow_positional=AllowPositional.ERROR,
    )
    def __init__(self, **kwargs):
        kwargs['name'] = 'states'
        state_types_table = popargs('state_types_table', kwargs)
        super().__init__(**kwargs)
        if self.state_type is not None and self.state_type.table is None:
            self.state_type.table = state_types_table

    @docval(
        {
            'name': 'state_type',
            'type': int,
            'doc': ('The state type for this state.'),
            'name': 'start_time',
            'type': float,
            'doc': ('The start time for the state'),
            'name': 'stop_time',
            'type': float,
            'doc': ('The stop time for the state'),
        },
        allow_extra=True,
        allow_positional=AllowPositional.ERROR,
    )
    def add_row(self, **kwargs):
        """Add a state to this table."""
        super().add_row(**kwargs)

    add_state = add_row  # alias for add_row

    def _generate_state_end_times(self, **kwargs):
        trials = kwargs['trials'] # [i['TrialPath'] for i in data['States']] *Note*: matlab_file=loadmat(beadl_path) ---> data=matlab_file['BeadlData']
        offset_times = kwargs['offset_times']
        end=[]
        for entry, time in zip(trials,offset_times):
            for i in range(len(entry)):
                if entry[i]['stateName']!= 'End':
                    end_time= entry[i+1]['stateStartTime']
                    end.append(float(end_time)+time)
                else:
                    end_time= entry[i]['stateStartTime']
                    end.append(float(end_time)+time)
        return end

    def _dict_to_list_conversion(self, **kwargs):
        data_dict= kwargs['data_dict']

        # 1) convert the list of dicts to list of lists containing the names.
        converted_data=[]
        for entry in data_dict:
            converted_data.append(list(itertools.chain.from_iterable([list(i.values()) for i in entry])))
        return converted_data

    def _all_states_validate(self, **kwargs):
        all_states= kwargs['all_states']

        # 1) convert the list of dicts to list of lists containing the names.
        converted_data=self._dict_to_list_conversion(data_dict=all_states)

        # 2) validate
        unique_keys=[]
        for k,g in itertools.groupby(converted_data):
            unique_keys.append(k)

        if len(unique_keys)>1:
            return False
        else:
            return True, unique_keys[0]

    @docval(
        {
            'name': 'data_path',
            'type': str,
            'doc': 'The path to the matlab data file.'
        }
    )
    def populate_from_matlab(self, **kwargs):
        state_types_table = self.state_type.table
        file_path = kwargs['data_path']

        matlab_file = loadmat(file_path)
        states_data = matlab_file['BeadlData']['States']
        offset_times = matlab_file['BeadlData']['SessionMetaData']['TrialStartOffset']


        #validate states_data AllStatesList
        all_states=[i['AllStatesList'] for i in states_data] # AllStatesList in data['States']
        validate_bool, unique_keys = self._all_states_validate(all_states=all_states)[0], self._all_states_validate(all_states=all_states)[1]

        if validate_bool:
            #validate state_types from matlab file with task program xml
            state_types_table_data = state_types_table['state_name'].data

            if sorted(unique_keys)==sorted(state_types_table_data):
                #retrieve start times
                updated_start_times=[]
                trials=[i['TrialPath'] for i in states_data]
                for trial,time in zip(trials, offset_times):
                    for state in trial:
                        new_time=float(state['stateStartTime']+time)
                        updated_start_times.append(new_time)

                trials_list = self._dict_to_list_conversion(data_dict=trials) # remove the dict structure
                trials_list_joined=list(itertools.chain.from_iterable(trials_list)) # join the lists
                start_times = [x for x in trials_list_joined if not isinstance(x, str)] # sort out the state names

                #generate end times
                end_times = self._generate_state_end_times(trials=trials, offset_times=offset_times)

                #dynamic table region for types todo:

                #formulate a list of states in order from the data
                trial_states = [x for x in trials_list_joined if isinstance(x, str)] # sort out the times

                #loop over list where we want to find the idx of each element in the state_types_table
                state_idx_list = []
                for trial_name in trial_states:
                    state_type_idx = state_types_table_data.index(trial_name)
                    state_idx_list.append(state_type_idx)

                #create a dynamic table region where the data is the idx
                region = state_types_table.create_region(name='type', region=state_idx_list, description='idx to the names of states')

                #TODO: Add check of same length for each of the 3 columns prior

                #populate states_table
                for i in range(len(end_times)):
                    self.add_row( state_type=region.data[i],start_time=updated_start_times[i], stop_time=end_times[i])

                return(self)

            else:
                msg = 'The states from the data does not match possible states from the task program.'
                raise ValueError(msg)
        else:
            msg = 'The AllStatesList column is invalid. Each entry must match.'
            raise ValueError(msg)


@register_class('EventsTable', 'ndx-beadl')
class EventsTable(DynamicTable):
    """A table to hold events data."""

    __columns__ = (
        {
            'name': 'timestamp',
            'description': ('The event timestamp'),
            'required': True
        },
        {
            'name': 'event_type',
            'description': ('The event type'),
            'table': True,
            'required': True
        },
        {
            'name': 'value',
            'description': ('The event value'),
            'required': True
        },
    )

    @docval(
        *get_docval(DynamicTable.__init__, 'id', 'columns', 'colnames'),
        {
            'name': 'description',
            'type': str,
            'doc': 'A table to hold events data.',
            'default': 'Event data',
        },
        {
            'name': 'event_types_table',
            'type': 'EventTypesTable',
            'doc': ('The events table.'),
            'default': None
        },
        allow_positional=AllowPositional.ERROR,
    )
    def __init__(self, **kwargs):
        kwargs['name'] = 'events'
        event_types_table = popargs('event_types_table', kwargs)
        super().__init__(**kwargs)
        if event_types_table is not None and self.event_type is not None and self.event_type.table is None:
            self.event_type.table = event_types_table

    @docval(
        {
            'name': 'event_type',
            'type': int,
            'doc': ('The event type.'),
        },
        {
            'name': 'value',
            'type': str,
            'doc': ('The event value.'),
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
        event_type_idx = kwargs['event_type']
        if event_type_idx >= 0 and event_type_idx < len(self.event_type.table):
            super().add_row(**kwargs)
        else:
            msg = 'Type index is out of bounds'
            raise ValueError(msg)

    add_event = add_row  # alias for add_row

    @docval(
        {
            'name': 'data_path',
            'type': str,
            'doc': 'The path to the matlab data file.'
        }
    )
    def populate_from_matlab(self, **kwargs):
        event_types_table = self.event_type.table
        file_path = kwargs['data_path']

        matlab_file = loadmat(file_path)
        events_data = matlab_file['BeadlData']['Events']
        offset_times = matlab_file['BeadlData']['SessionMetaData']['TrialStartOffset']

        event_times=[]
        event_names_data=[]
        event_value=[]
        for trial, time in zip(events_data, offset_times):
            for event in trial['AllEvents']:
                event_names_data.append(event['eventName'])
                event_times.append(event['eventTime']+time)
                event_value.append(event['eventValue'])

        unique_event_names=list(set(event_names_data))
        event_types_table_data = event_types_table['event_name'].data

        if sorted(unique_event_names)==sorted(event_types_table_data):
            #loop over event_names where we want to find the idx of each element in the event_types_table
            event_idx_list = []
            for event_name in event_names_data:
                event_type_idx = event_types_table_data.index(event_name)
                event_idx_list.append(event_type_idx)

            #create a dynamic table region where the data is the idx
            region = event_types_table.create_region(name='event_type', region=event_idx_list, description='idx to the names of events')

            #populate events_table
            for i in range(len(event_times)):
                self.add_row(timestamp=event_times[i], event_type=region.data[i], value=event_value[i])

            return(self)
        else:
            msg = 'The events from the data does not match possible events from the task program.'
            raise ValueError(msg)


@register_class('StateTypesTable', 'ndx-beadl')
class StateTypesTable(DynamicTable):
    __columns__ = (
        {
        'name': 'state_name',
        'description': ('The name of the state type'),
        'required': True
        },
    )

    @docval(
        *get_docval(DynamicTable.__init__, 'id', 'columns', 'colnames'),
        {
            'name': 'description',
            'type': str,
            'doc': 'A table for the state_types',
            'default': 'state type data',
        },
        {'name': 'beadl_task_program', 'type': BEADLTaskProgram,
         'doc': 'the BEADLTaskProgram used', 'default': None},
        {'name': 'populate_from_program', 'type': bool, 'doc': 'Boolean to populate from task program.',
         'default': False})
    def __init__(self, **kwargs):
        kwargs['name'] = 'state_types'
        beadl_task_program = popargs('beadl_task_program', kwargs)
        populate_from_program = popargs('populate_from_program', kwargs)
        super().__init__(**kwargs)
        self.beadl_task_program = beadl_task_program
        if self.beadl_task_program == None:
            self.populate_from_program = False
        else:
            self.populate_from_program = populate_from_program

        if self.populate_from_program:
            self._populate_from_program()

    def _populate_from_program(self):
        parsed_xml_object = BeadlXMLParser(string=self.beadl_task_program.data)
        element=parsed_xml_object.element(element_name='BeadlStates')
        parsed_states = parsed_xml_object._parse_protocal_children(element=element)

        for state in parsed_states['BeadlState']:
            super().add_row(state_name=state['name'])

@register_class('EventTypesTable', 'ndx-beadl')
class EventTypesTable(DynamicTable):
    __columns__ = (
        {
        'name': 'event_name',
        'description': ('The name of the event type'),
        'required': True
        },
    )

    @docval(
        *get_docval(DynamicTable.__init__, 'id', 'columns', 'colnames'),
        {
            'name': 'description',
            'type': str,
            'doc': 'A table for the event_types',
            'default': 'state type data',
        },
        {'name': 'beadl_task_program', 'type': BEADLTaskProgram,
         'doc': 'the BEADLTaskProgram used', 'default': None},
        {'name': 'populate_from_program', 'type': bool, 'doc': 'Boolean to populate from task program.',
         'default': False})
    def __init__(self, **kwargs):
        kwargs['name'] = 'event_types'
        beadl_task_program = popargs('beadl_task_program', kwargs)
        populate_from_program = popargs('populate_from_program', kwargs)
        super().__init__(**kwargs)
        self.beadl_task_program = beadl_task_program
        if self.beadl_task_program == None:
            self.populate_from_program = False
        else:
            self.populate_from_program = populate_from_program
        if self.populate_from_program:
            self._populate_from_program()

    def _populate_from_program(self):
        parsed_xml_object = BeadlXMLParser(string=self.beadl_task_program.data)

        # HardwareEvents
        element=parsed_xml_object.element(element_name='BeadlEvents')
        parsed_states = parsed_xml_object._parse_protocal_children(element=element)
        hardware_events = parsed_states['HardwareEvent']

        # Events within states
        element=parsed_xml_object.element(element_name='BeadlStates')
        parsed_states = parsed_xml_object._parse_protocal_children(element=element)
        possible_events = ['ExternalEvent', 'TimerEvent', 'ArgumentEvent', 'VariableEvent', 'TimeSpanEvent']

        events_from_states=[]
        for event in possible_events:
            events_from_states+=(parsed_states[event])

        # joined events
        joined_events = hardware_events+events_from_states

        for event_name in set([event['eventName'] for event in joined_events]):
            super().add_row(event_name=event_name)

@register_class('ActionTypesTable', 'ndx-beadl')
class ActionTypesTable(DynamicTable):
    __columns__ = (
        {
        'name': 'action_name',
        'description': ('The name of the action type'),
        'required': True
        },
    )

    @docval(
        *get_docval(DynamicTable.__init__, 'id', 'columns', 'colnames'),
        {
            'name': 'description',
            'type': str,
            'doc': 'A table for the action_types',
            'default': 'Action type data',
        },
        {'name': 'beadl_task_program', 'type': BEADLTaskProgram,
         'doc': 'the BEADLTaskProgram used', 'default': None},
        {'name': 'populate_from_program', 'type': bool, 'doc': 'Boolean to populate from task program.',
         'default': False})
    def __init__(self, **kwargs):
        kwargs['name'] = 'action_types'
        beadl_task_program = popargs('beadl_task_program', kwargs)
        populate_from_program = popargs('populate_from_program', kwargs)
        super().__init__(**kwargs)
        self.beadl_task_program = beadl_task_program
        if self.beadl_task_program == None:
            self.populate_from_program = False
        else:
            self.populate_from_program = populate_from_program
        if self.populate_from_program:
            self._populate_from_program()

    def _populate_from_program(self):
        parsed_xml_object = BeadlXMLParser(string=self.beadl_task_program.data)
        element=parsed_xml_object.element(element_name='BeadlStates')
        parsed_states = parsed_xml_object._parse_protocal_children(element=element)
        possible_actions = ['OutputAction', 'SetVariableAction', 'CallbackAction']

        actions_from_states=[]
        for action in possible_actions:
            actions_from_states+=(parsed_states[action])


        for action in set([action['actionName'] for action in actions_from_states]):
            super().add_row(action_name=action)


@register_class('ActionsTable', 'ndx-beadl')
class ActionsTable(DynamicTable):
    __columns__ = (
        {
            'name': 'timestamp',
            'description': ('The action time'),
            'required': True
        },
        {
            'name': 'action_type',
            'description': ('The action type'),
            'table': True,
            'required': True
        },
        {
            'name': 'value',
            'description': ('The action value'),
            'required': True
        },
    )

    @docval(
        *get_docval(DynamicTable.__init__, 'id', 'columns', 'colnames'),
        {
            'name': 'description',
            'type': str,
            'doc': 'A table to hold the action data.',
            'default': 'OutputAction data',
        },
        {
            'name': 'action_types_table',
            'type': 'ActionTypesTable',
            'doc': ('The ActionTypesTable.'),
            'default': None
        },
        allow_positional=AllowPositional.ERROR,
    )
    def __init__(self, **kwargs):
        kwargs['name'] = 'actions'
        action_types_table = popargs('action_types_table', kwargs)
        super().__init__(**kwargs)
        if action_types_table is not None and self.action_type is not None and self.action_type.table is None:
            self.action_type.table = action_types_table

    @docval(
        {
            'name': 'action_type',
            'type': int,
            'doc': ('The action type.'),
        },
        {
            'name': 'value',
            'type': str,
            'doc': ('The action value.'),
        },
        {
            'name': 'timestamp',
            'type': float,
            'doc': ('The action time.'),
        },
        allow_extra=True,
        allow_positional=AllowPositional.ERROR,
    )
    def add_row(self, **kwargs):
        """Add an event to this table."""
        action_type_idx = kwargs['action_type']
        if action_type_idx >= 0 and action_type_idx < len(self.action_type.table):
            super().add_row(**kwargs)
        else:
            msg = 'Type index is out of bounds'
            raise ValueError(msg)

    add_action = add_row  # alias for add_row

    @docval(
        {
            'name': 'data_path',
            'type': str,
            'doc': 'The path to the matlab data file.'
        }
    )
    def populate_from_matlab(self, **kwargs):
        action_types_table = self.action_type.table
        file_path = kwargs['data_path'] # data

        matlab_file = loadmat(file_path)
        states_data = matlab_file['BeadlData']['States']
        offset_times = matlab_file['BeadlData']['SessionMetaData']['TrialStartOffset']

        action_times=[]
        action_names_data=[]
        action_value=[]
        for trial, time in zip(states_data, offset_times):
            trial_actions=trial['StateOutputActions']
            if type(trial_actions)!= list:
                trial_actions=[trial_actions]
            for action in trial_actions:
                action_names_data.append(action['actionName'])
                action_times.append(float(action['actionTime'])+time)
                action_value.append(action['actionValue'])

        #validate set-up
        unique_action_names=list(set(action_names_data))
        action_types_table_data = action_types_table['action_name'].data

        if sorted(unique_action_names)==sorted(action_types_table_data):
            #loop over event_names where we want to find the idx of each element in the event_types_table
            action_idx_list = []
            for action_name in action_names_data:
                action_type_idx = action_types_table_data.index(action_name)
                action_idx_list.append(action_type_idx)

            #create a dynamic table region where the data is the idx
            region = action_types_table.create_region(name='action_type', region=action_idx_list, description='idx to the names of actions')

            #populate events_table
            for i in range(len(action_times)):
                self.add_row(action_type=region.data[i], value=action_value[i], timestamp=action_times[i])

            return(self)
        else:
            msg = 'The actions from the data does not match possible actions from the task program.'
            raise ValueError(msg)


@register_class('ASE', 'ndx-beadl')
class ASE(NWBDataInterface):

    __fields__ = (
        {'name': 'actions', 'child': True},
        {'name': 'states', 'child': True},
        {'name': 'events', 'child': True},
        )

    """
    A container class to store the ActionsTable, StatesTable, and EventsTable.
    This class will be added into acquisition within the NWBFile, rather than the
    individual tables themselves.
    """
    @docval({'name': 'actions',
             'type': ActionsTable,
             'doc': 'The populated ActionsTable to be added to the NWBFile.'},
            {'name': 'states',
             'type': StatesTable,
             'doc': 'The populated StatesTable to be added to the NWBFile.'},
            {'name': 'events',
             'type': EventsTable,
             'doc': 'The populated EventsTable to be added to the NWBFile.'},)
    def __init__(self, **kwargs):
        kwargs['name'] = 'ASE'
        actions, states, events = popargs('actions',
                                          'states',
                                          'events',
                                          kwargs)
        super().__init__(**kwargs)
        self.__actions = actions
        self.__states = states
        self.__events = events

    @property
    def actions(self):
        return self.__actions

    @property
    def states(self):
        return self.__states

    @property
    def events(self):
        return self.__events
