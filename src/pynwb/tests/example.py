from ndx_beadl import (Task, BEADLTaskProgram, BEADLTaskSchema, EventTypesTable, EventsTable,
                       StateTypesTable, StatesTable, TrialsTable, ActionTypesTable, ActionsTable, TaskArgumentsTable)
from ndx_beadl.beadl_xml_parser import BeadlXMLParser
from pynwb import NWBHDF5IO
from pynwb.file import NWBFile, Subject
import datetime
import os

# Input file paths with the example BEADL data
base_dir = os.path.dirname(os.path.abspath(__file__))
beadl_task_schema_file = os.path.join(base_dir, "BEADL.xsd")
beadl_task_program_file = os.path.join(base_dir, "LightChasingTask.xml")
bead_data_file = os.path.join(base_dir, "BeadlDataSample.mat")

# Output file paths
nwb_filepath = "beadl_light_chasing_task.nwb"

# Import the BEADL task schema and task program
with open(beadl_task_schema_file, "r") as test_xsd_file:
    test_xsd = test_xsd_file.read()

with open(beadl_task_program_file, "r") as test_xml_file:
    test_xml = test_xml_file.read()

beadl_task_schema = BEADLTaskSchema(
    name='beadl_task_schema',
    data=test_xsd,
    version="0.1.0",
    language="XSD"
)

beadl_task_program = BEADLTaskProgram(
    name='beadl_task_program',
    data=test_xml,
    schema=beadl_task_schema,
    language="XML"
)

# Create a new Tasks object and add the BEADL task metadata
task_arg_table = TaskArgumentsTable(beadl_task_program=beadl_task_program, populate_from_program=True)
event_types = EventTypesTable(description="description", beadl_task_program=beadl_task_program,
                              populate_from_program=True)
action_types = ActionTypesTable(description="description", beadl_task_program=beadl_task_program,
                                populate_from_program=True)
state_types = StateTypesTable(description="description", beadl_task_program=beadl_task_program,
                              populate_from_program=True)

task = Task(
    beadl_task_program=beadl_task_program,
    beadl_task_schema=beadl_task_schema,
    event_types=event_types,
    state_types=state_types,
    action_types=action_types,
    task_arguments=task_arg_table
)

# Create Events, Actions, and States
events = EventsTable(description="description", event_types_table=event_types)
_ = events.populate_from_matlab(data_path=bead_data_file)

actions = ActionsTable(description="description", action_types_table=action_types)
_ = actions.populate_from_matlab(data_path=bead_data_file)

states = StatesTable(description="description", state_types_table=state_types)
_ = states.populate_from_matlab(data_path=bead_data_file)

trials = TrialsTable(description="description", states_table=states, events_table=events, actions_table=actions)
_ = trials.populate_from_matlab(data_path=bead_data_file)

# Create NWBFile
nwbfile = NWBFile(
    session_description="session_description",
    identifier="LightChasingTask",
    session_start_time=datetime.datetime.now(datetime.timezone.utc),
    subject=Subject(subject_id="SP_W2_RH")
)
# Add Beadl Data
nwbfile.add_lab_meta_data(task)
nwbfile.add_acquisition(states)
nwbfile.add_acquisition(events)
nwbfile.add_acquisition(actions)
nwbfile.trials = trials

# Write the NWBFile
with NWBHDF5IO(nwb_filepath, mode="w") as io:
    io.write(nwbfile)

# Read the NWBFile
io = NWBHDF5IO(nwb_filepath, mode="r")
read_nwbfile = io.read()
