# ndx-beadl Extension for NWB

The extension *ndx_beadl* defines a collection of interlinked table data structures for
storing behavioral tasks and data. While the extension has been designed with BEADL in 
mind, the data structures are general and are intended to be useful even without BEADL. 
For additional information about BEADL, please visit [https://beadl.org/](https://beadl.org/).

The *ndx-beadl* data model consists of three main components:

![ndx-beadl schema](docs/tutorial_nwb_userdays_2022/beadl_components_p1.png?raw=true "ndx-beadl schema")
![ndx-beadl schema](docs/tutorial_nwb_userdays_2022/beadl_components_p2.png?raw=true "ndx-beadl schema")


## Installation

```python
git clone https://github.com/rly/ndx-beadl.git
cd ndx-beadl
pip install -e . 
```

## Usage

```python 
from ndx_beadl import (Task, BEADLTaskProgram, BEADLTaskSchema, EventTypesTable, EventsTable,
                       StateTypesTable, StatesTable, TrialsTable, ActionTypesTable, ActionsTable, TaskArgumentTable)
from ndx_beadl.beadl_xml_parser import BeadlXMLParser
from pynwb import NWBFile, NWBHDF5IO

# Import the BEADL task schema and task program
with open("src/pynwb/tests/beadl_schema_file", "r") as test_xsd_file:
    test_xsd = test_xsd_file.read()

with open("src/pynwb/tests/beadl_task_file", "r") as test_xml_file:
    test_xml = test_xml_file.read()

beadl_task_schema = BEADLTaskSchema(
    name = 'beadl_task_schema',
    data=test_xsd,
    version="0.1.0",
    language="XSD"
)

beadl_task_program = BEADLTaskProgram(
    name = 'beadl_task_program',
    data=test_xml,
    schema=beadl_task_schema,
    language="XML"
)

# Create a new Tasks object and add the BEADL task metadata
task_arg_table=TaskArgumentTable(beadl_task_program=beadl_task_program, populate_from_program=True)
event_types = EventTypesTable(description="description", beadl_task_program=beadl_task_program, populate_from_program=True)
action_types= ActionTypesTable(description="description", beadl_task_program=beadl_task_program, populate_from_program=True)
state_types = StateTypesTable(description="description", beadl_task_program=beadl_task_program, populate_from_program=True)

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
_ = events.populate_from_matlab(data_path=beadl_path)

actions = ActionsTable(description="description", action_types_table=action_types)
_ = actions.populate_from_matlab(data_path=beadl_path)

states = StatesTable(description="description", state_types_table=state_types)
_ = states.populate_from_matlab(data_path=beadl_path)

trials = TrialsTable(description="description", states_table=states, events_table=events, actions_table=actions)
_ = trials.populate_from_matlab(data_path=beadl_path)

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

# Write and Read the NWBFile
with NWBHDF5IO(nwb_filepath, mode="w") as io:
    io.write(nwbfile)
    
io = NWBHDF5IO(nwb_filepath, mode="r")
read_nwbfile = io.read()

```
---
This extension was created using [ndx-template](https://github.com/nwb-extensions/ndx-template).
