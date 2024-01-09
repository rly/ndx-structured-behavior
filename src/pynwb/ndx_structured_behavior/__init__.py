import os
from pynwb import load_namespaces, get_class

# Set path of the namespace.yaml file to the expected install location
ndx_structured_behavior_specpath = os.path.join(
    os.path.dirname(__file__),
    'spec',
    'ndx-structured-behavior.namespace.yaml'
)

# If the extension has not been installed yet but we are running directly from
# the git repo
if not os.path.exists(ndx_structured_behavior_specpath):
    ndx_structured_behavior_specpath = os.path.abspath(os.path.join(
        os.path.dirname(__file__),
        '..', '..', '..',
        'spec',
        'ndx-structured-behavior.namespace.yaml'
    ))

# Load the namespace
load_namespaces(ndx_structured_behavior_specpath)

TaskSchema = get_class('TaskSchema', 'ndx-structured-behavior')
BEADLTaskSchema = get_class('BEADLTaskSchema', 'ndx-structured-behavior')
TaskProgram = get_class('TaskProgram', 'ndx-structured-behavior')
BEADLTaskProgram = get_class('BEADLTaskProgram', 'ndx-structured-behavior')
from .trials_table import (EventsTable, StatesTable, TrialsTable, StateTypesTable, EventTypesTable,
                           ActionTypesTable, ActionsTable, data_program_validator)  # noqa: F401,E402
from .task_argument_table import TaskArgumentsTable

# TaskRecording uses EventsTable, StatesTable, TrialsTable and so those classes must be registered
# before TaskRecording is generated and registered
TaskRecording = get_class('TaskRecording', 'ndx-structured-behavior')
Task = get_class('Task', 'ndx-structured-behavior')
