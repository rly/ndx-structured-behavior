from pynwb import NWBHDF5IO, NWBFile
from pynwb.core import DynamicTableRegion
from pynwb.device import Device
from pynwb.ecephys import ElectrodeGroup
from pynwb.file import ElectrodeTable as get_electrode_table
from pynwb.testing import TestCase, remove_test_file, AcquisitionH5IOMixin

from ndx_structured_behavior import (Task, BEADLTaskProgram, BEADLTaskSchema, EventTypesTable, EventsTable,
                       StateTypesTable, StatesTable, TrialsTable)


with open("BEADL.xsd", "r") as test_xsd_file:
    test_xsd = test_xsd_file.read()

with open("LightChasingTask.xml", "r") as test_xml_file:
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

# tasks = Tasks(
#     task_programs=[beadl_task_program],
#     task_schemas=[beadl_task_schema]
# )

state_types = StateTypesTable(description="description", beadl_task_program=beadl_task_program, populate_from_program=True)
states = StatesTable(description="description", state_types_table=state_types)
states.populate_from_matlab(data_path=beadl_path)
