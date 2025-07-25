from importlib.resources import files
from pynwb import load_namespaces, get_class

# Get path to the namespace.yaml file with the expected location when installed not in editable mode
__location_of_this_file = files(__name__)
__spec_path = __location_of_this_file / "spec" / "ndx-structured-behavior.namespace.yaml"

# If that path does not exist, we are likely running in editable mode. Use the local path instead
if not __spec_path.exists():
    __spec_path = __location_of_this_file.parent.parent.parent / "spec" / "ndx-structured-behavior.namespace.yaml"

# Load the namespace
load_namespaces(str(__spec_path))

TaskSchema = get_class('TaskSchema', 'ndx-structured-behavior')
BEADLTaskSchema = get_class('BEADLTaskSchema', 'ndx-structured-behavior')
TaskProgram = get_class('TaskProgram', 'ndx-structured-behavior')
BEADLTaskProgram = get_class('BEADLTaskProgram', 'ndx-structured-behavior')

from .trials_table import (EventsTable, StatesTable, TrialsTable, StateTypesTable, EventTypesTable,
                           ActionTypesTable, ActionsTable, data_program_validator)  # noqa: F401, E402
from .task_argument_table import TaskArgumentsTable

# TaskRecording uses EventsTable, StatesTable, TrialsTable and so those classes must be registered
# before TaskRecording is generated and registered
TaskRecording = get_class('TaskRecording', 'ndx-structured-behavior')
Task = get_class('Task', 'ndx-structured-behavior')


# TODO: Add all classes to __all__ to make them accessible at the package level
__all__ = [
    "TetrodeSeries",
    "TaskSchema",
    "BEADLTaskSchema",
    "TaskProgram",
    "BEADLTaskProgram",
    "EventsTable",
    "StatesTable",
    "TrialsTable",
    "StateTypesTable",
    "EventTypesTable",
    "ActionTypesTable",
    "ActionsTable",
    "data_program_validator",
    "TaskArgumentsTable",
    "TaskRecording",
    "Task",
]

# Remove these functions/modules from the package
del load_namespaces, get_class, files, __location_of_this_file, __spec_path
