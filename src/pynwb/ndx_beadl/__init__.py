import os
from pynwb import load_namespaces, get_class

# Set path of the namespace.yaml file to the expected install location
ndx_beadl_specpath = os.path.join(
    os.path.dirname(__file__),
    'spec',
    'ndx-beadl.namespace.yaml'
)

# If the extension has not been installed yet but we are running directly from
# the git repo
if not os.path.exists(ndx_beadl_specpath):
    ndx_beadl_specpath = os.path.abspath(os.path.join(
        os.path.dirname(__file__),
        '..', '..', '..',
        'spec',
        'ndx-beadl.namespace.yaml'
    ))

# Load the namespace
load_namespaces(ndx_beadl_specpath)

TaskSchema = get_class('TaskSchema', 'ndx-beadl')
BEADLTaskSchema = get_class('BEADLTaskSchema', 'ndx-beadl')
TaskProgram = get_class('TaskProgram', 'ndx-beadl')
BEADLTaskProgram = get_class('BEADLTaskProgram', 'ndx-beadl')
from .trials_table import Task, EventsTable, StatesTable, TrialsTable, StateTypesTable, EventTypesTable, ActionTypesTable, ActionsTable  # noqa: F401,E402
from .task_argument_table import TaskArgumentsTable
