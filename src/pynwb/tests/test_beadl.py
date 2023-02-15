import datetime
import numpy as np
import os
import subprocess
import sys

from pynwb import NWBHDF5IO, NWBFile
from pynwb.core import DynamicTableRegion
from pynwb.device import Device
from pynwb.ecephys import ElectrodeGroup
from pynwb.file import ElectrodeTable as get_electrode_table
from pynwb.testing import TestCase, remove_test_file, AcquisitionH5IOMixin

from ndx_beadl import (Task, BEADLTaskProgram, BEADLTaskSchema, EventTypesTable, EventsTable,
                       StateTypesTable, StatesTable, TrialsTable, ActionTypesTable, ActionsTable,
                       TaskArgumentsTable)
from ndx_beadl.plot import show_by_type_and_value



DATA_BASE_DIR = os.path.dirname(os.path.abspath(__file__))
BEADL_TASK_SCHEMA_FILE = os.path.join(DATA_BASE_DIR, "BEADL.xsd")
BEADL_TASK_PROGRAM_FILE = os.path.join(DATA_BASE_DIR, "LightChasingTask.xml")
BEADL_DATA_FILE = os.path.join(DATA_BASE_DIR, "BeadlDataSample.mat")


def set_up_nwbfile():
    nwbfile = NWBFile(
        session_description="session_description",
        identifier="identifier",
        session_start_time=datetime.datetime.now(datetime.timezone.utc)
    )

    return nwbfile


class TestExampleScript(TestCase):
    """Test running the example script"""
    def setUp(self):
        self.test_script = os.path.join(DATA_BASE_DIR, "example.py")
        self.nwb_outfile_path = os.path.join(DATA_BASE_DIR,  "beadl_light_chasing_task.nwb")
        # Make sure we don't have a left-over file from a previous test run
        if os.path.exists(self.nwb_outfile_path):
            os.remove(self.nwb_outfile_path)

    def tearDown(self):
        if os.path.exists(self.nwb_outfile_path):
            os.remove(self.nwb_outfile_path)

    def test_run_example_script(self):
        # Run the example script
        subprocess.run([sys.executable, self.test_script])
        # Test that the output file was generated
        self.assertTrue(os.path.exists(self.nwb_outfile_path))
        # Check that the data in the file is correct
        with NWBHDF5IO(self.nwb_outfile_path, "r") as io:
            nwbfile = io.read()
            # Currently just checking that the data tables exists and have the correct number of rows
            self.assertEqual(len(nwbfile.acquisition['actions']), 251)
            self.assertEqual(len(nwbfile.acquisition['events']), 7695)
            self.assertEqual(len(nwbfile.acquisition['states']), 612)
            self.assertEqual(len(nwbfile.trials), 153)

class TestBEADLProgramConstructors(TestCase):
    # TODO split into separate tests

    def setUp(self):
        """Set up an NWB file. Necessary because BEADL objects will be added to LabMetaData."""
        self.nwbfile = set_up_nwbfile()

    def test_constructor(self):
        """Test that the constructor for BEADLTaskSchema, BEADLTaskProgram, and Tasks set values as expected."""
        with open(BEADL_TASK_SCHEMA_FILE , "r") as test_xsd_file:
            test_xsd = test_xsd_file.read()

        with open(BEADL_TASK_PROGRAM_FILE, "r") as test_xml_file:
            test_xml = test_xml_file.read()

        beadl_task_schema = BEADLTaskSchema(
            name = "beadl_task_schema",
            data=test_xsd,
            version="0.1.0",
            language="XSD"  # TODO remove when no longer necessary
        )

        beadl_task_program = BEADLTaskProgram(
            name = "beadl_task_program",
            data=test_xml,
            schema=beadl_task_schema,
            language="XML"  # TODO remove when no longer necessary
        )

        self.assertEqual(beadl_task_schema.name, "beadl_task_schema")
        self.assertEqual(beadl_task_schema.data, test_xsd)
        self.assertEqual(beadl_task_schema.version, "0.1.0")
        self.assertEqual(beadl_task_schema.language, "XSD")
        self.assertEqual(beadl_task_program.name, "beadl_task_program")
        self.assertEqual(beadl_task_program.data, test_xml)
        self.assertIs(beadl_task_program.schema, beadl_task_schema)
        self.assertEqual(beadl_task_program.language, "XML")

class TestBEADLTableConstructors(TestCase):

    def setUp(self):
        """Set up an NWB file. Necessary because BEADL objects will be added to LabMetaData."""
        self.nwbfile = set_up_nwbfile()

    def test_constructor(self):
        with open(BEADL_TASK_SCHEMA_FILE , "r") as test_xsd_file:
            test_xsd = test_xsd_file.read()

        with open(BEADL_TASK_PROGRAM_FILE, "r") as test_xml_file:
            test_xml = test_xml_file.read()

        beadl_task_schema = BEADLTaskSchema(
            name = "beadl_task_schema",
            data=test_xsd,
            version="0.1.0",
            language="XSD"  # TODO remove when no longer necessary
        )

        beadl_task_program = BEADLTaskProgram(
            name = "beadl_task_program",
            data=test_xml,
            schema=beadl_task_schema,
            language="XML"  # TODO remove when no longer necessary
        )

        task_arg_table=TaskArgumentsTable(beadl_task_program=beadl_task_program, populate_from_program=True)

        action_types = ActionTypesTable(description="description", beadl_task_program=beadl_task_program, populate_from_program=True)

        actions = ActionsTable(description="description", action_types_table=action_types)
        actions.add_action(action_type=0, timestamp=0.4, value="open")
        actions.add_action(action_type=1, timestamp=0.5, value="open")

        event_types = EventTypesTable(description="description", beadl_task_program=beadl_task_program, populate_from_program=True) #assert description

        events = EventsTable(description="description", event_types_table=event_types)
        events.add_event(event_type=0, timestamp=0.4, value="on")
        events.add_event(event_type=1, timestamp=0.5, value="on")
        events.add_event(event_type=1, timestamp=1.4, value="on")
        events.add_event(event_type=0, timestamp=1.5, value="on")

        state_types = StateTypesTable(description="description", beadl_task_program=beadl_task_program, populate_from_program=True)

        states = StatesTable(description="description", state_types_table=state_types)

        states.add_state(state_type=0, start_time=0.0, stop_time=0.1)
        states.add_state(state_type=1, start_time=0.1, stop_time=0.2)
        states.add_state(state_type=2, start_time=0.2, stop_time=0.4)
        states.add_state(state_type=3, start_time=0.4, stop_time=0.5)
        states.add_state(state_type=0, start_time=1.0, stop_time=1.1)
        states.add_state(state_type=1, start_time=1.1, stop_time=1.2)
        states.add_state(state_type=2, start_time=1.2, stop_time=1.4)
        states.add_state(state_type=3, start_time=1.4, stop_time=1.5)

        trials = TrialsTable(description="description", states_table=states, events_table=events, actions_table=actions)
        trials.add_trial(start_time=0.0, stop_time=0.8, states=[0, 1, 2, 3], events=[0, 1], actions=[0,1])
        trials.add_trial(start_time=1.0, stop_time=1.8, states=[4, 5, 6, 7], events=[2, 3], actions=[0,1])

        task = Task(
                beadl_task_program=beadl_task_program,
                beadl_task_schema=beadl_task_schema,
                event_types=event_types,
                state_types=state_types,
                action_types=action_types,
                task_arguments=task_arg_table
            )

        self.assertEqual(trials.description, "description")
        self.assertEqual(states.description, "description")
        self.assertEqual(events.description, "description")
        self.assertEqual(event_types.description, "description")
        self.assertEqual(state_types.description, "description")
        #
        self.assertEqual(trials.columns[0].data, [0,1])
        self.assertEqual(trials.columns[1].data, [0.8,1.8])
        self.assertEqual(trials.colnames, ("start_time", "stop_time", "states", "events", "actions"))

        self.assertEqual(states.columns[0].data, [0.0, 0.1, 0.2, 0.4, 1.0, 1.1, 1.2, 1.4])
        self.assertEqual(states.columns[1].data, [0.1, 0.2, 0.4, 0.5, 1.1, 1.2, 1.4, 1.5])
        self.assertEqual(states.columns[2].data, [0, 1, 2, 3, 0, 1, 2, 3])

        self.assertEqual(events.columns[0].data, [0.4, 0.5, 1.4, 1.5])
        self.assertEqual(events.columns[1].data, [0, 1, 1, 0])
        self.assertEqual(events.columns[2].data, ["on", "on", "on", "on"])

        self.assertEqual(actions.columns[0].data, [0.4, 0.5])
        self.assertEqual(actions.columns[1].data, [0, 1])
        self.assertEqual(actions.columns[2].data, ["open", "open"])

        self.assertEqual(set(action_types.columns[0].data), set(["CorrectPortLED", "CorrectPortValve"]))

        self.assertEqual(set(state_types.columns[0].data), set(["WaitForPoke", "End", "Reward", "ITI", "TimeOut"]))
        self.assertEqual(state_types.beadl_task_program.data, test_xml)

        self.assertEqual(set(event_types.columns[0].data), set(["ErrorPort2Poke", "stateTimer", "ErrorPort1Poke", "CorrectPortPoke"]))
        self.assertEqual(event_types.beadl_task_program.data, test_xml)


class TestBeadlTablesPopulate(TestCase):
    def setUp(self):
        with open(BEADL_TASK_SCHEMA_FILE , "r") as test_xsd_file:
            test_xsd = test_xsd_file.read()

        with open(BEADL_TASK_PROGRAM_FILE, "r") as test_xml_file:
            test_xml = test_xml_file.read()

        self.beadl_task_schema = BEADLTaskSchema(
            name = "beadl_task_schema",
            data=test_xsd,
            version="0.1.0",
            language="XSD"  # TODO remove when no longer necessary
        )

        self.beadl_task_program = BEADLTaskProgram(
            name = "beadl_task_program",
            data=test_xml,
            schema=self.beadl_task_schema,
            language="XML"  # TODO remove when no longer necessary
        )

        self.beadl_data = BEADL_DATA_FILE

    def test_populate_from_matlab(self):
        action_types = ActionTypesTable(description="description", beadl_task_program=self.beadl_task_program, populate_from_program=True)

        actions = ActionsTable(description="description", action_types_table=action_types)
        actions.populate_from_matlab(data_path=self.beadl_data)

        event_types = EventTypesTable(description="description", beadl_task_program=self.beadl_task_program, populate_from_program=True) #assert description

        events = EventsTable(description="description", event_types_table=event_types)
        events.populate_from_matlab(data_path=self.beadl_data)

        state_types = StateTypesTable(description="description", beadl_task_program=self.beadl_task_program, populate_from_program=True)

        states = StatesTable(description="description", state_types_table=state_types)
        states.populate_from_matlab(data_path=self.beadl_data)

        trials = TrialsTable(description="description", states_table=states, events_table=events, actions_table=actions)
        trials.populate_from_matlab(data_path=self.beadl_data)

        self.assertEqual(events.to_dataframe().shape, (7695, 3))
        self.assertEqual(actions.to_dataframe().shape, (251, 3))
        self.assertEqual(states.to_dataframe().shape, (612, 3))
        self.assertEqual(trials.to_dataframe().shape, (153, 10))


class TestPlot(TestCase):

    def setUp(self):
        with open(BEADL_TASK_SCHEMA_FILE , "r") as test_xsd_file:
            test_xsd = test_xsd_file.read()

        with open(BEADL_TASK_PROGRAM_FILE, "r") as test_xml_file:
            test_xml = test_xml_file.read()

        self.beadl_task_schema = BEADLTaskSchema(
            name = "beadl_task_schema",
            data=test_xsd,
            version="0.1.0",
            language="XSD"  # TODO remove when no longer necessary
        )

        self.beadl_task_program = BEADLTaskProgram(
            name = "beadl_task_program",
            data=test_xml,
            schema=self.beadl_task_schema,
            language="XML"  # TODO remove when no longer necessary
        )

        self.beadl_data = BEADL_DATA_FILE

        self.action_types = ActionTypesTable(description="description", beadl_task_program=self.beadl_task_program, populate_from_program=True)

        self.actions = ActionsTable(description="description", action_types_table=self.action_types)
        self.actions.populate_from_matlab(data_path=self.beadl_data)

        self.event_types = EventTypesTable(description="description", beadl_task_program=self.beadl_task_program, populate_from_program=True) #assert description

        self.events = EventsTable(description="description", event_types_table=self.event_types)
        self.events.populate_from_matlab(data_path=self.beadl_data)

    def test_events_show_by_type_and_value(self):
        y_values, y_tick_labels, y_label = show_by_type_and_value(table=self.events, table_types=self.event_types)

        self.assertEqual(y_label, "Event type")
        self.assertEqual(sorted(y_tick_labels), sorted(["ErrorPort1Poke(out)", "CorrectPortPoke(out)", "ErrorPort1Poke(in)", "ErrorPort2Poke(in)",
                                         "ErrorPort2Poke(out)",
                                         "CorrectPortPoke(in)",
                                         "stateTimer(expired)"]))

    def test_events_show_by_type(self):
        y_values, y_tick_labels, y_label = show_by_type_and_value(table=self.events, table_types=self.event_types, show_table_values=False)

        self.assertEqual(y_label, "Event type")
        self.assertEqual(sorted(y_tick_labels), sorted(["ErrorPort1Poke", "CorrectPortPoke", "stateTimer", "ErrorPort2Poke"]))

    def test_actions_show_by_type_and_value(self):
        y_values, y_tick_labels, y_label = show_by_type_and_value(table=self.actions, table_types=self.action_types)

        self.assertEqual(y_label, "Action type")
        self.assertEqual(sorted(y_tick_labels), sorted(["CorrectPortLED(on)", "CorrectPortValve(open)"]))

    def test_actions_show_by_type(self):
        y_values, y_tick_labels, y_label = show_by_type_and_value(table=self.actions, table_types=self.action_types, show_table_values=False)

        self.assertEqual(y_label, "Action type")
        self.assertEqual(sorted(y_tick_labels), sorted(["CorrectPortValve", "CorrectPortLED"]))


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

        with open(BEADL_TASK_SCHEMA_FILE , "r") as test_xsd_file:
            test_xsd = test_xsd_file.read()

        with open(BEADL_TASK_PROGRAM_FILE, "r") as test_xml_file:
            test_xml = test_xml_file.read()

        beadl_task_schema = BEADLTaskSchema(
            name = "beadl_task_schema", # why do we need this?
            data=test_xsd,
            version="0.1.0",
            language="XSD"  # TODO remove when no longer necessary
        )

        beadl_task_program = BEADLTaskProgram(
            name = "beadl_task_program", # why do we need this?
            data=test_xml,
            schema=beadl_task_schema,
            language="XML"  # TODO remove when no longer necessary
        )

        task_arg_table=TaskArgumentsTable(beadl_task_program=beadl_task_program, populate_from_program=True)

        action_types = ActionTypesTable(description="description", beadl_task_program=beadl_task_program, populate_from_program=True)

        actions = ActionsTable(description="description", action_types_table=action_types)
        actions.add_action(action_type=0, timestamp=0.4, value="open")
        actions.add_action(action_type=1, timestamp=0.5, value="open")

        event_types = EventTypesTable(description="description", beadl_task_program=beadl_task_program, populate_from_program=True) #assert description

        events = EventsTable(description="description", event_types_table=event_types)
        events.add_event(event_type=0, timestamp=0.4, value="on")
        events.add_event(event_type=1, timestamp=0.5, value="on")
        events.add_event(event_type=1, timestamp=1.4, value="on")
        events.add_event(event_type=0, timestamp=1.5, value="on")

        state_types = StateTypesTable(description="description", beadl_task_program=beadl_task_program, populate_from_program=True)

        states = StatesTable(description="description", state_types_table=state_types)

        states.add_state(state_type=0, start_time=0.0, stop_time=0.1)
        states.add_state(state_type=1, start_time=0.1, stop_time=0.2)
        states.add_state(state_type=2, start_time=0.2, stop_time=0.4)
        states.add_state(state_type=3, start_time=0.4, stop_time=0.5)
        states.add_state(state_type=0, start_time=1.0, stop_time=1.1)
        states.add_state(state_type=1, start_time=1.1, stop_time=1.2)
        states.add_state(state_type=2, start_time=1.2, stop_time=1.4)
        states.add_state(state_type=3, start_time=1.4, stop_time=1.5)

        trials = TrialsTable(description="description", states_table=states, events_table=events, actions_table=actions)
        trials.add_trial(start_time=0.0, stop_time=0.8, states=[0, 1, 2, 3], events=[0, 1], actions=[0,1])
        trials.add_trial(start_time=1.0, stop_time=1.8, states=[4, 5, 6, 7], events=[2, 3], actions=[0,1])

        task = Task(
                beadl_task_program=beadl_task_program,
                beadl_task_schema=beadl_task_schema,
                event_types=event_types,
                state_types=state_types,
                action_types=action_types,
                task_arguments=task_arg_table
            )

        self.nwbfile.trials = trials

        file_task = self.nwbfile.add_lab_meta_data(task)
        self.nwbfile.add_acquisition(states)
        self.nwbfile.add_acquisition(events)
        self.nwbfile.add_acquisition(actions)

        with NWBHDF5IO(self.path, mode="w") as io:
            io.write(self.nwbfile)

        with NWBHDF5IO(self.path, mode="r", load_namespaces=True) as io:
            read_nwbfile = io.read()
            self.assertContainerEqual(file_task, read_nwbfile.lab_meta_data["task"])
            self.assertContainerEqual(actions, read_nwbfile.get_acquisition("actions"))
            self.assertContainerEqual(events, read_nwbfile.get_acquisition("events"))
            self.assertContainerEqual(states, read_nwbfile.get_acquisition("states"))
