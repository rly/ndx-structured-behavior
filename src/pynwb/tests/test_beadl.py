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
        with open("src/pynwb/tests/BEADL.xsd", "r") as test_xsd_file:
            test_xsd = test_xsd_file.read()

        with open("src/pynwb/tests/Foraging_Task.xml", "r") as test_xml_file:
            test_xml = test_xml_file.read()

        beadl_task_schema = BEADLTaskSchema(
            data=test_xsd,
            version="0.1.0",
            language="XSD"  # TODO remove when no longer necessary
        )

        beadl_task_program = BEADLTaskProgram(
            data=test_xml,
            schema=beadl_task_schema,
            language="XML"  # TODO remove when no longer necessary
        )

        tasks = Tasks(
            task_program=beadl_task_program,
            task_schema=beadl_task_schema
        )

        self.nwbfile.add_lab_meta_data(tasks)

        self.assertEqual(beadl_task_schema.name, "task_schema")
        self.assertEqual(beadl_task_schema.data, test_xsd)
        self.assertEqual(beadl_task_schema.version, "0.1.0")
        self.assertEqual(beadl_task_schema.language, "XSD")
        self.assertEqual(beadl_task_program.name, "task_program")
        self.assertEqual(beadl_task_program.data, test_xml)
        self.assertIs(beadl_task_program.schema, beadl_task_schema)
        self.assertEqual(beadl_task_program.language, "XML")

        self.assertEqual(tasks.name, "tasks")
        self.assertIs(tasks.task_schema, beadl_task_schema)
        self.assertIs(tasks.task_program, beadl_task_program)


class TestBEADLTableConstructors(TestCase):

    def setUp(self):
        """Set up an NWB file. Necessary because BEADL objects will be added to LabMetaData."""
        self.nwbfile = set_up_nwbfile()

    # def test_constructor(self):
    #     event_types = EventTypesTable(description="")
    #     event_types.add_row(event_name="leftPortIn")
    #     event_types.add_row(event_name="rightPortIn")
    #
    #     events = EventsTable(description="")
    #     events.add_event(type=0, timestamp=0.4)
    #     events.add_event(type=1, timestamp=0.5)
    #     events.add_event(type=1, timestamp=1.4)
    #     events.add_event(type=0, timestamp=1.5)
    #
    #     state_types = StateTypesTable(description="")
    #     state_types.add_row(state_name="InitTrial")
    #     state_types.add_row(state_name="TriggerBridge")
    #     state_types.add_row(state_name="WaitForBridge")
    #     state_types.add_row(state_name="Pre")
    #
    #     states = StatesTable(description="")
    #     states.add_state(type=0, start_time=0.0, stop_time=0.1)
    #     states.add_state(type=1, start_time=0.1, stop_time=0.2)
    #     states.add_state(type=2, start_time=0.2, stop_time=0.4)
    #     states.add_state(type=3, start_time=0.4, stop_time=0.5)
    #     states.add_state(type=0, start_time=1.0, stop_time=1.1)
    #     states.add_state(type=1, start_time=1.1, stop_time=1.2)
    #     states.add_state(type=2, start_time=1.2, stop_time=1.4)
    #     states.add_state(type=3, start_time=1.4, stop_time=1.5)
    #
    #     trials = TrialsTable(description="")
    #     trials.add_trial(start_time=0.0, stop_time=0.8, states=[0, 1, 2, 3], events=[0, 1],
    #                      states_table=states, events_table=events)
    #     trials.add_trial(start_time=1.0, stop_time=1.8, states=[4, 5, 6, 7], events=[2, 3])
    #
    #     self.nwbfile.trials = trials
    #     self.nwbfile.add_acquisition(states)  # TODO move to time intervals after merge
    #     self.nwbfile.add_acquisition(state_types)
    #     self.nwbfile.add_acquisition(events)
    #     self.nwbfile.add_acquisition(event_types)

#
# class TestTetrodeSeriesRoundtrip(TestCase):
#     """Simple roundtrip test for TetrodeSeries."""
#
#     def setUp(self):
#         self.nwbfile = set_up_nwbfile()
#         self.path = "test.nwb"
#
#     def tearDown(self):
#         remove_test_file(self.path)
#
#     def test_roundtrip(self):
#         """
#         Add a TetrodeSeries to an NWBFile, write it to file, read the file, and test that the TetrodeSeries from the
#         file matches the original TetrodeSeries.
#         """
#         all_electrodes = self.nwbfile.create_electrode_table_region(
#             region=list(range(0, 10)),
#             description="all the electrodes"
#         )
#
#         data = np.random.rand(100, 3)
#         tetrode_series = TetrodeSeries(
#             name="TetrodeSeries",
#             description="description",
#             data=data,
#             rate=1000.,
#             electrodes=all_electrodes,
#             trode_id=1
#         )
#
#         self.nwbfile.add_acquisition(tetrode_series)
#
#         with NWBHDF5IO(self.path, mode="w") as io:
#             io.write(self.nwbfile)
#
#         with NWBHDF5IO(self.path, mode="r", load_namespaces=True) as io:
#             read_nwbfile = io.read()
#             self.assertContainerEqual(tetrode_series, read_nwbfile.acquisition["TetrodeSeries"])
#
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
