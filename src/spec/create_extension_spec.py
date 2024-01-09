# -*- coding: utf-8 -*-
import os.path

from pynwb.spec import NWBNamespaceBuilder, export_spec, NWBGroupSpec, NWBDatasetSpec, NWBAttributeSpec, NWBRefSpec


def main():
    # these arguments were auto-generated from your cookiecutter inputs
    ns_builder = NWBNamespaceBuilder(
        doc="""An NWB extension for storing BEADL programs and data""",
        name="""ndx-structured-behavior""",
        version="""0.1.0""",
        author=list(map(str.strip, """Ryan Ly, Matthew Avaylon, Oliver Ruebel, Michael Wulf""".split(','))),
        contact=list(map(str.strip, """rly@lbl.gov, mavaylon@lbl.gov,
                                       oruebel@lbl.gov, michael.wulf@wustl.edu """.split(',')))
    )

    ns_builder.include_namespace('core')

    # TODO this is being written as a group spec
    task_program = NWBDatasetSpec(
        neurodata_type_def='TaskProgram',
        neurodata_type_inc='NWBData',
        doc=('A dataset to store a task program.'),
        dtype='text',
        attributes=[
            NWBAttributeSpec(
                name='language',
                doc=('The language of the program. Currently only "XML" is supported. It is not recommended to '
                     'include executable code here.'),
                dtype='text'
            ),
            NWBAttributeSpec(
                name='schema',
                doc='The task schema that governs the program.',
                dtype=NWBRefSpec(
                    target_type='TaskSchema',
                    reftype='object'
                )
            )
        ],
    )

    beadl_task_program = NWBDatasetSpec(
        neurodata_type_def='BEADLTaskProgram',
        neurodata_type_inc='TaskProgram',
        doc=('A dataset to store a BEADL task program.'),
        attributes=[
            NWBAttributeSpec(
                name='language',
                doc='The language of the program, fixed to "XML".',
                dtype='text',
                default_value='XML'
            ),
            NWBAttributeSpec(
                name='schema',
                doc='The BEADL task schema that governs the program.',
                dtype=NWBRefSpec(
                    target_type='BEADLTaskSchema',
                    reftype='object'
                )
            ),
        ],
    )

    task_schema = NWBDatasetSpec(
        neurodata_type_def='TaskSchema',
        neurodata_type_inc='NWBData',
        doc=('A dataset to store a task schema, e.g., an XSD file.'),
        dtype='text',
        attributes=[
            NWBAttributeSpec(
                name='version',
                doc='The version of the schema',
                dtype='text'
            ),
            NWBAttributeSpec(
                name='language',
                doc=('The language of the schema. Currently only "XSD" is supported.'),
                dtype='text',
            ),
        ],
    )

    beadl_task_schema = NWBDatasetSpec(
        neurodata_type_def='BEADLTaskSchema',
        neurodata_type_inc='TaskSchema',
        doc=('A dataset to store a BEADL task schema.'),
        attributes=[
            NWBAttributeSpec(
                name='language',
                doc='The language of the schema, fixed to "XSD".',
                dtype='text',
                default_value='XSD'  # TODO change to value
            ),
        ],
    )

    action_types_table = NWBGroupSpec(
        name='action_types',
        neurodata_type_def='ActionTypesTable',
        neurodata_type_inc='DynamicTable',
        doc=('A column-based table to store information about action_types, one type per row.'),
        datasets=[
            NWBDatasetSpec(
                name='action_name',
                neurodata_type_inc='VectorData',
                doc=('The name of the action'),
            ),
        ],
    )

    event_types_table = NWBGroupSpec(
        name='event_types',
        neurodata_type_def='EventTypesTable',
        neurodata_type_inc='DynamicTable',
        doc=('A column-based table to store information about action_types, one type per row.'),
        datasets=[
            NWBDatasetSpec(
                name='event_name',
                neurodata_type_inc='VectorData',
                doc=('The name of the event'),
            ),
        ],
    )

    state_types_table = NWBGroupSpec(
        name='state_types',
        neurodata_type_def='StateTypesTable',
        neurodata_type_inc='DynamicTable',
        doc=('A column-based table to store information about action_types, one type per row.'),
        datasets=[
            NWBDatasetSpec(
                name='state_name',
                neurodata_type_inc='VectorData',
                doc=('The name of the state'),
            ),
        ],
    )

    task_argument_table = NWBGroupSpec(
        name='task_arguments',
        neurodata_type_def='TaskArgumentsTable',
        neurodata_type_inc='DynamicTable',
        doc='Table to hold Task Program arguments.',
        datasets=[
            NWBDatasetSpec(
                name='argument_name',
                neurodata_type_inc='VectorData',
                dtype='text',
                doc=('The names of the arguments'),
            ),
            NWBDatasetSpec(
                name='argument_description',
                neurodata_type_inc='VectorData',
                dtype='text',
                doc=('The comment of the argument from the program'),
            ),
            NWBDatasetSpec(
                name='expression',
                neurodata_type_inc='VectorData',
                dtype='text',
                doc=('The expression/value (as a string) of the argument'),
            ),
            NWBDatasetSpec(
                name='expression_type',
                neurodata_type_inc='VectorData',
                dtype='text',
                doc=('The type of the argument value.'),
            ),
            NWBDatasetSpec(
                name='output_type',
                neurodata_type_inc='VectorData',
                dtype='text',
                doc=('The intended final type of the argument value.'),
            ),
        ]
    )

    tasks = NWBGroupSpec(
        name='task',
        neurodata_type_def='Task',
        neurodata_type_inc='LabMetaData',
        doc=('A group to store task-related general metadata. TODO When merged with core, this will no longer '
             'inherit from LabMetaData but from NWBContainer and be placed optionally in /general.'),
        groups=[
            NWBGroupSpec(
                name='event_types',
                neurodata_type_inc='EventTypesTable',
                doc=('The EventTypesTable')
            ),
            NWBGroupSpec(
                name='state_types',
                neurodata_type_inc='StateTypesTable',
                doc=('The StateTypesTable')
            ),
            NWBGroupSpec(
                name='action_types',
                neurodata_type_inc='ActionTypesTable',
                doc=('The ActionTypesTable')
            ),
            NWBGroupSpec(
                name='task_arguments',
                neurodata_type_inc='TaskArgumentsTable',
                doc=('The TaskArgumentsTable')
            )

        ],
        datasets=[
            NWBDatasetSpec(
                # TODO requiring this name is restrictive, especially when the task program is called BEADLTaskProgram
                # name='task_program',
                neurodata_type_inc='TaskProgram',
                doc=('A dataset to store a task program.'),
                # quantity='?'
            ),
            NWBDatasetSpec(
                # TODO requiring this name is restrictive
                # name='task_schema',
                neurodata_type_inc='TaskSchema',
                doc=('A dataset to store a task schema, e.g., an XSD file.'),
                # quantity='?'
            ),
        ]
    )

    # TODO force the DTR/VectorIndex targets to be specific data types

    trials_table = NWBGroupSpec(
        name='trials',
        neurodata_type_def='TrialsTable',
        neurodata_type_inc='TimeIntervals',
        doc=('A column-based table to store information about trials, one trial per row.'),
        datasets=[
            NWBDatasetSpec(
                name='states',
                neurodata_type_inc='DynamicTableRegion',
                doc=('The states that occurred on each trial. This is represented as a ragged array reference to '
                     'rows of the States table.'),
            ),
            NWBDatasetSpec(
                name='states_index',
                neurodata_type_inc='VectorIndex',
                doc=('VectorIndex for the "states" column.'),
                quantity='?',
            ),
            NWBDatasetSpec(
                name='events',
                neurodata_type_inc='DynamicTableRegion',
                doc=('The events that occurred on each trial. This is represented as a ragged array reference to '
                     'rows of the Events table.'),
            ),
            NWBDatasetSpec(
                name='events_index',
                neurodata_type_inc='VectorIndex',
                doc=('VectorIndex for the "events" column.'),
                quantity='?',
            ),
            NWBDatasetSpec(
                name='actions',
                neurodata_type_inc='DynamicTableRegion',
                doc=('The actions that occurred on each trial. This is represented as a ragged array reference to '
                     'rows of the Actions table.'),
            ),
            NWBDatasetSpec(
                name='actions_index',
                neurodata_type_inc='VectorIndex',
                doc=('VectorIndex for the "actions" column.'),
                quantity='?',
            ),
        ]
    )

    states_table = NWBGroupSpec(
        name='states',
        neurodata_type_def='StatesTable',
        neurodata_type_inc='TimeIntervals',
        doc=('A column-based table to store information about states, one state per row.'),
        datasets=[
            NWBDatasetSpec(
                name='state_type',
                neurodata_type_inc='DynamicTableRegion',
                doc=('The type of state that occurred on each trial. This is represented as a reference to '
                     'a row of the StateTypesTable.'),
            ),
            # NWBDatasetSpec(
            #     name='start_time',
            #     neurodata_type_inc='VectorData',
            #     doc=('The start time that the state'),
            # ),
            # NWBDatasetSpec(
            #     name='stop_time',
            #     neurodata_type_inc='VectorData',
            #     doc=('The stop time that the state'),
            # ),
        ]
    )

    events_table = NWBGroupSpec(
        name='events',
        neurodata_type_def='EventsTable',
        neurodata_type_inc='DynamicTable',
        doc=('A column-based table to store information about events, one event per row.'),
        datasets=[
            NWBDatasetSpec(
                name='timestamp',
                neurodata_type_inc='VectorData',
                dtype='float32',
                doc=('The time that the event occurred, in seconds.'),
            ),
            NWBDatasetSpec(
                name='event_type',
                neurodata_type_inc='DynamicTableRegion',
                doc=('The type of event that occurred on each trial. This is represented as a reference to '
                     'a row of the EventTypesTable.'),
            ),
            NWBDatasetSpec(
                name='value',
                neurodata_type_inc='VectorData',
                dtype='text',
                doc=('The value of the event'),
            ),
        ]
    )

    actions_table = NWBGroupSpec(
        name='actions',
        neurodata_type_def='ActionsTable',
        neurodata_type_inc='DynamicTable',
        doc=('A column-based table to store information about actions, one action per row.'),
        datasets=[
            NWBDatasetSpec(
                name='timestamp',
                neurodata_type_inc='VectorData',
                dtype='float32',
                doc=('The time that the action occurred, in seconds.'),
            ),
            NWBDatasetSpec(
                name='action_type',
                neurodata_type_inc='DynamicTableRegion',
                doc=('The type of action that occurred on each trial. This is represented as a reference to '
                     'a row of the ActionTypesTable.'),
            ),
            NWBDatasetSpec(
                name='value',
                neurodata_type_inc='VectorData',
                dtype='text',
                doc=('The value of the action'),
            ),
        ]
    )

    task_recording = NWBGroupSpec(
        name='task_recording',
        neurodata_type_def='TaskRecording',
        neurodata_type_inc='NWBDataInterface',
        doc='A group to store the ActionsTable, StatesTable, EventsTable.',
        groups=[
            NWBGroupSpec(
                name='events',
                neurodata_type_inc='EventsTable',
                doc=('The EventsTable')
            ),
            NWBGroupSpec(
                name='states',
                neurodata_type_inc='StatesTable',
                doc=('The StatesTable')
            ),
            NWBGroupSpec(
                name='actions',
                neurodata_type_inc='ActionsTable',
                doc=('The ActionsTable')
            )
        ]
    )

    new_data_types = [task_program, task_recording, beadl_task_program, task_schema, beadl_task_schema, tasks,
                      trials_table, state_types_table, states_table, event_types_table, events_table,
                      actions_table, action_types_table, task_argument_table]

    # export the spec to yaml files in the spec folder
    output_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'spec'))
    export_spec(ns_builder, new_data_types, output_dir)


if __name__ == '__main__':
    # usage: python create_extension_spec.py
    main()
