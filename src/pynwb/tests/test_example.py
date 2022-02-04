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


class TestExample(TestCase):

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

        event_types = EventTypesTable(description="description") #assert description
        event_types.add_row(event_name="leftPortIn")
        event_types.add_row(event_name="rightPortIn")

        events = EventsTable(description="description", event_types_table=event_types)
        events.add_event(type=0, timestamp=0.4)
        events.add_event(type=1, timestamp=0.5)
        events.add_event(type=1, timestamp=1.4)
        events.add_event(type=0, timestamp=1.5)

        state_types = StateTypesTable(description="description")
        state_types.add_row(state_name="InitTrial")
        state_types.add_row(state_name="TriggerBridge")
        state_types.add_row(state_name="WaitForBridge")
        state_types.add_row(state_name="Pre")

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

        with NWBHDF5IO("test_file.nwb", "w") as io:
            io.write(self.nwbfile)
