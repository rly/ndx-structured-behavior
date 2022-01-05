# -*- coding: utf-8 -*-
import os.path

from pynwb.spec import NWBNamespaceBuilder, export_spec, NWBGroupSpec, NWBDatasetSpec, NWBAttributeSpec, NWBRefSpec


def main():
    # these arguments were auto-generated from your cookiecutter inputs
    ns_builder = NWBNamespaceBuilder(
        doc="""An NWB extension for storing BEADL programs and data""",
        name="""ndx-beadl""",
        version="""0.1.0""",
        author=list(map(str.strip, """Ryan Ly""".split(','))),
        contact=list(map(str.strip, """rly@lbl.gov""".split(',')))
    )

    ns_builder.include_type('NWBData', namespace='core')
    ns_builder.include_type('LabMetaData', namespace='core')
    ns_builder.include_type('TimeIntervals', namespace='core')
    ns_builder.include_type('DynamicTable', namespace='hdmf-common')
    ns_builder.include_type('VectorData', namespace='hdmf-common')
    ns_builder.include_type('VectorIndex', namespace='hdmf-common')
    ns_builder.include_type('DynamicTableRegion', namespace='hdmf-common')

    # TODO this is being written as a group spec
    task_program = NWBDatasetSpec(
        name='task_program',  # TODO remove this because it should not be required to name a TaskProgram this
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
        ],
    )

    task_schema = NWBDatasetSpec(
        name='task_schema',  # TODO remove this because it should not be required to name a TaskProgram this
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

    tasks = NWBGroupSpec(
        name='tasks',
        neurodata_type_def='Tasks',
        neurodata_type_inc='LabMetaData',
        doc=('A group to store task-related general metadata. TODO When merged with core, this will no longer '
             'inherit from LabMetaData but from NWBContainer and be placed optionally in /general.'),
        datasets=[
            NWBDatasetSpec(
                name='task_program',  # TODO look into whether this is compatible with setting name on TaskProgram
                neurodata_type_inc='TaskProgram',
                doc=('A dataset to store a task program.'),
            ),
            NWBDatasetSpec(
                name='task_schema',
                neurodata_type_inc='TaskSchema',
                doc=('A dataset to store a task schema, e.g., an XSD file.'),
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
                quantity='?',
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
                quantity='?',
            ),
            NWBDatasetSpec(
                name='events_index',
                neurodata_type_inc='DynamicTableRegion',
                doc=('VectorIndex for the "events" column.'),
                quantity='?',
            ),
        ]
    )

    state_types_table = NWBGroupSpec(
        name='state_types',
        neurodata_type_def='StateTypesTable',
        neurodata_type_inc='DynamicTable',
        doc=('A column-based table to store information about state types, one state type per row.'),
        datasets=[
            NWBDatasetSpec(
                name='state_name',
                neurodata_type_inc='VectorData',
                dtype='text',
                doc=('The name of the state.'),
            ),
            # TODO link to a specific part of the task program
        ]
    )

    states_table = NWBGroupSpec(
        name='states',
        neurodata_type_def='StatesTable',
        neurodata_type_inc='TimeIntervals',
        doc=('A column-based table to store information about states, one state per row.'),
        datasets=[
            NWBDatasetSpec(
                name='type',
                neurodata_type_inc='DynamicTableRegion',
                doc=('The type of state that occurred on each trial. This is represented as a reference to '
                     'a row of the StateTypesTable.'),
            ),
        ]
    )

    event_types_table = NWBGroupSpec(
        name='event_types',
        neurodata_type_def='EventTypesTable',
        neurodata_type_inc='DynamicTable',
        doc=('A column-based table to store information about event types, one event type per row.'),
        datasets=[
            NWBDatasetSpec(
                name='event_name',
                neurodata_type_inc='VectorData',
                dtype='text',
                doc=('The name of the event.'),
            ),
            # TODO link to a specific part of the task program
        ]
    )

    events_table = NWBGroupSpec(
        name='events',
        neurodata_type_def='EventsTable',
        neurodata_type_inc='DynamicTable',
        doc=('A column-based table to store information about events, one event per row.'),
        datasets=[
            NWBDatasetSpec(
                name='type',
                neurodata_type_inc='DynamicTableRegion',
                doc=('The type of event that occurred on each trial. This is represented as a reference to '
                     'a row of the EventTypesTable.'),
            ),
            NWBDatasetSpec(
                name='timestamp',
                neurodata_type_inc='VectorData',
                dtype='float32',
                doc=('The time that the event occurred, in seconds.'),
            ),
        ]
    )

    new_data_types = [task_program, beadl_task_program, task_schema, beadl_task_schema, tasks,
                      trials_table, state_types_table, states_table, event_types_table, events_table]

    # export the spec to yaml files in the spec folder
    output_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'spec'))
    export_spec(ns_builder, new_data_types, output_dir)


if __name__ == '__main__':
    # usage: python create_extension_spec.py
    main()
