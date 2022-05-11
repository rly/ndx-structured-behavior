import datetime
import numpy as np

from pynwb import NWBHDF5IO, NWBFile
from pynwb.core import DynamicTableRegion
from pynwb.device import Device
from pynwb.ecephys import ElectrodeGroup
from pynwb.file import ElectrodeTable as get_electrode_table
from pynwb.testing import TestCase, remove_test_file, AcquisitionH5IOMixin

from ndx_beadl import (Tasks, BEADLTaskProgram, BEADLTaskSchema, EventTypesTable, EventsTable,
                       StateTypesTable, StatesTable, TrialsTable)


def set_up_nwbfile():
    nwbfile = NWBFile(
        session_description="session_description",
        identifier="identifier",
        session_start_time=datetime.datetime.now(datetime.timezone.utc)
    )

    return nwbfile


class TestBEADLProgramConstructors(TestCase):
    # TODO split into separate tests

    def setUp(self):
        """Set up an NWB file. Necessary because BEADL objects will be added to LabMetaData."""
        self.nwbfile = set_up_nwbfile()

    def test_constructor(self):
        """Test that the constructor for BEADLTaskSchema, BEADLTaskProgram, and Tasks set values as expected."""
        with open("/Users/mavaylon/Research/NWB/ndx-beadl/src/pynwb/tests/BEADL.xsd", "r") as test_xsd_file:
            test_xsd = test_xsd_file.read()

        with open("/Users/mavaylon/Research/NWB/ndx-beadl/src/pynwb/tests/Foraging_Task.xml", "r") as test_xml_file:
            test_xml = test_xml_file.read()

        beadl_task_schema = BEADLTaskSchema(
            name = 'beadl_task_schema',
            data=test_xsd,
            version="0.1.0",
            language="XSD"  # TODO remove when no longer necessary
        )

        beadl_task_program = BEADLTaskProgram(
            name = 'beadl_task_program',
            data=test_xml,
            schema=beadl_task_schema,
            language="XML"  # TODO remove when no longer necessary
        )

        tasks = Tasks(
            task_programs=[beadl_task_program],
            task_schemas=[beadl_task_schema]
        )

        self.nwbfile.add_lab_meta_data(tasks)

        self.assertEqual(beadl_task_schema.name, "beadl_task_schema")
        self.assertEqual(beadl_task_schema.data, test_xsd)
        self.assertEqual(beadl_task_schema.version, "0.1.0")
        self.assertEqual(beadl_task_schema.language, "XSD")
        self.assertEqual(beadl_task_program.name, "beadl_task_program")
        self.assertEqual(beadl_task_program.data, test_xml)
        self.assertIs(beadl_task_program.schema, beadl_task_schema)
        self.assertEqual(beadl_task_program.language, "XML")

        self.assertEqual(tasks.name, "tasks")
        self.assertEqual(tasks.task_schemas, {'beadl_task_schema': beadl_task_schema})
        self.assertEqual(tasks.task_programs, {'beadl_task_program': beadl_task_program})


class TestBEADLTableConstructors(TestCase):

    def setUp(self):
        """Set up an NWB file. Necessary because BEADL objects will be added to LabMetaData."""
        self.nwbfile = set_up_nwbfile()

    def test_constructor(self):
        with open("/Users/mavaylon/Research/NWB/ndx-beadl/src/pynwb/tests/BEADL.xsd", "r") as test_xsd_file:
            test_xsd = test_xsd_file.read()

        with open("/Users/mavaylon/Research/NWB/ndx-beadl/src/pynwb/tests/Foraging_Task.xml", "r") as test_xml_file:
            test_xml = test_xml_file.read()

        beadl_task_schema = BEADLTaskSchema(
            name = 'beadl_task_schema',
            data=test_xsd,
            version="0.1.0",
            language="XSD"  # TODO remove when no longer necessary
        )

        beadl_task_program = BEADLTaskProgram(
            name = 'beadl_task_program',
            data=test_xml,
            schema=beadl_task_schema,
            language="XML"  # TODO remove when no longer necessary
        )

        event_types = EventTypesTable(description="description", beadl_task_program=beadl_task_program, populate_from_program=True) #assert description

        events = EventsTable(description="description", event_types_table=event_types)
        events.add_event(type=0, timestamp=0.4)
        events.add_event(type=1, timestamp=0.5)
        events.add_event(type=1, timestamp=1.4)
        events.add_event(type=0, timestamp=1.5)

        state_types = StateTypesTable(description="description", beadl_task_program=beadl_task_program, populate_from_program=True)

        states = StatesTable(description="description", state_types_table=state_types)
        states.add_state(type=0, start_time=0.0, stop_time=0.1)
        states.add_state(type=1, start_time=0.1, stop_time=0.2)
        states.add_state(type=2, start_time=0.2, stop_time=0.4)
        states.add_state(type=3, start_time=0.4, stop_time=0.5)
        states.add_state(type=0, start_time=1.0, stop_time=1.1)
        states.add_state(type=1, start_time=1.1, stop_time=1.2)
        states.add_state(type=2, start_time=1.2, stop_time=1.4)
        states.add_state(type=3, start_time=1.4, stop_time=1.5)

        trials = TrialsTable(description="description", states_table=states, events_table=events)
        trials.add_trial(start_time=0.0, stop_time=0.8, states=[0, 1, 2, 3], events=[0, 1])
        trials.add_trial(start_time=1.0, stop_time=1.8, states=[4, 5, 6, 7], events=[2, 3])

        self.assertEqual(trials.description, "description")
        self.assertEqual(states.description, "description")
        self.assertEqual(events.description, "description")
        self.assertEqual(event_types.description, "description")
        self.assertEqual(state_types.description, "description")

        self.assertEqual(trials.columns[0].data, [0,1])
        self.assertEqual(trials.columns[1].data, [0.8,1.8])
        self.assertEqual(trials.colnames, ('start_time', 'stop_time', 'states', 'events'))

        self.assertEqual(states.columns[0].data, [0.0, 0.1, 0.2, 0.4, 1.0, 1.1, 1.2, 1.4])
        self.assertEqual(states.columns[1].data, [0.1, 0.2, 0.4, 0.5, 1.1, 1.2, 1.4, 1.5])
        self.assertEqual(states.columns[2].data, [0, 1, 2, 3, 0, 1, 2, 3])

        self.assertEqual(events.columns[0].data, [0, 1, 1, 0])
        self.assertEqual(events.columns[1].data, [0.4, 0.5, 1.4, 1.5])

        self.assertEqual(state_types.columns[0].data, ['InitTrial', 'TriggerBridge', 'WaitForBridge', 'Pre', 'WaitForPoke', 'LeftRewardDelay', 'LeftReward', 'LeftDrinking', 'RightRewardDelay', 'RightReward', 'RightDrinking'])
        self.assertEqual(state_types.beadl_task_program.data, test_xml)

        self.assertEqual(event_types.columns[0].data, ['bridgeChanged', 'leftPortIn', 'rightPortIn'])
        self.assertEqual(event_types.beadl_task_program.data, test_xml)

class TestTaskSeriesRoundtrip(TestCase):
    """Simple roundtrip test for TetrodeSeries."""

    def setUp(self):
        self.nwbfile = set_up_nwbfile()
        self.path = "test.nwb"

    def tearDown(self):
        remove_test_file(self.path)

    def test_roundtrip(self):
        """
        Add a Task to an NWBFile, write it to file, read the file, and test that the Task from the
        file matches the original Task.
        """

        with open("/Users/mavaylon/Research/NWB/ndx-beadl/src/pynwb/tests/BEADL.xsd", "r") as test_xsd_file:
            test_xsd = test_xsd_file.read()

        with open("/Users/mavaylon/Research/NWB/ndx-beadl/src/pynwb/tests/Foraging_Task.xml", "r") as test_xml_file:
            test_xml = test_xml_file.read()

        beadl_task_schema = BEADLTaskSchema(
            name = 'beadl_task_schema', # why do we need this?
            data=test_xsd,
            version="0.1.0",
            language="XSD"  # TODO remove when no longer necessary
        )

        beadl_task_program = BEADLTaskProgram(
            name = 'beadl_task_program', # why do we need this?
            data=test_xml,
            schema=beadl_task_schema,
            language="XML"  # TODO remove when no longer necessary
        )

        tasks = Tasks(
            task_programs=[beadl_task_program],
            task_schemas=[beadl_task_schema]
        )

        event_types = EventTypesTable(description="description", beadl_task_program=tasks.task_programs['beadl_task_program'], populate_from_program=True) #assert description

        events = EventsTable(description="description", event_types_table=event_types)
        events.add_event(type=0, timestamp=0.4)
        events.add_event(type=1, timestamp=0.5)
        events.add_event(type=1, timestamp=1.4)
        events.add_event(type=0, timestamp=1.5)

        state_types = StateTypesTable(description="description", beadl_task_program=tasks.task_programs['beadl_task_program'], populate_from_program=True)

        states = StatesTable(description="description", state_types_table=state_types)
        states.add_state(type=0, start_time=0.0, stop_time=0.1)
        states.add_state(type=1, start_time=0.1, stop_time=0.2)
        states.add_state(type=2, start_time=0.2, stop_time=0.4)
        states.add_state(type=3, start_time=0.4, stop_time=0.5)
        states.add_state(type=0, start_time=1.0, stop_time=1.1)
        states.add_state(type=1, start_time=1.1, stop_time=1.2)
        states.add_state(type=2, start_time=1.2, stop_time=1.4)
        states.add_state(type=3, start_time=1.4, stop_time=1.5)

        trials = TrialsTable(description="description", states_table=states, events_table=events)
        trials.add_trial(start_time=0.0, stop_time=0.8, states=[0, 1, 2, 3], events=[0, 1])
        trials.add_trial(start_time=1.0, stop_time=1.8, states=[4, 5, 6, 7], events=[2, 3])

        self.nwbfile.trials = trials
        self.nwbfile.add_acquisition(states)  # TODO move to time intervals after merge
        self.nwbfile.add_acquisition(state_types)
        self.nwbfile.add_acquisition(events)
        self.nwbfile.add_acquisition(event_types)

        file_tasks = self.nwbfile.add_lab_meta_data(tasks)

        with NWBHDF5IO(self.path, mode="w") as io:
            io.write(self.nwbfile)

        with NWBHDF5IO(self.path, mode="r", load_namespaces=True) as io:
            read_nwbfile = io.read()
            self.assertContainerEqual(file_tasks, read_nwbfile.lab_meta_data["tasks"])
            self.assertContainerEqual(event_types, read_nwbfile.get_acquisition("event_types"))
            self.assertContainerEqual(events, read_nwbfile.get_acquisition("events"))
            self.assertContainerEqual(state_types, read_nwbfile.get_acquisition("state_types"))
            self.assertContainerEqual(states, read_nwbfile.get_acquisition("states"))


#
# class TestTetrodeSeriesRoundtripPyNWB(AcquisitionH5IOMixin, TestCase):
#     """Complex, more complete roundtrip test for TetrodeSeries using pynwb.testing infrastructure."""
#
#     def setUpContainer(self):
#         """ Return the test TetrodeSeries to read/write """
#         self.device = Device(
#             name="device_name"
#         )
#
#         self.group = ElectrodeGroup(
#             name="electrode_group",
#             description="description",
#             location="location",
#             device=self.device
#         )
#
#         self.table = get_electrode_table()  # manually create a table of electrodes
#         for i in np.arange(10.):
#             self.table.add_row(
#                 x=i,
#                 y=i,
#                 z=i,
#                 imp=np.nan,
#                 location="location",
#                 filtering="filtering",
#                 group=self.group,
#                 group_name="electrode_group"
#             )
#
#         all_electrodes = DynamicTableRegion(
#             data=list(range(0, 10)),
#             description="all the electrodes",
#             name="electrodes",
#             table=self.table
#         )
#
#         data = np.random.rand(100, 3)
#         tetrode_series = TetrodeSeries(
#             name="name",
#             description="description",
#             data=data,
#             rate=1000.,
#             electrodes=all_electrodes,
#             trode_id=1
#         )
#         return tetrode_series
#
#     def addContainer(self, nwbfile):
#         """Add the test TetrodeSeries and related objects to the given NWBFile."""
#         nwbfile.add_device(self.device)
#         nwbfile.add_electrode_group(self.group)
#         nwbfile.set_electrode_table(self.table)
#         nwbfile.add_acquisition(self.container)
