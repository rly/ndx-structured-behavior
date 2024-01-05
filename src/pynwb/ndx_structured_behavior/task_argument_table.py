from pynwb import register_class
from pynwb.core import DynamicTable
from hdmf.utils import docval, get_docval, getargs, popargs, AllowPositional
from hdmf.container import Row
from ndx_structured_behavior import BEADLTaskProgram
from .beadl_xml_parser import BeadlXMLParser

@register_class('TaskArgumentsTable', 'ndx-structured-behavior')
class TaskArgumentsTable(DynamicTable):
    """
    A table to hold Task Program arguments.
    """

    __columns__ = (
        {
            'name': 'argument_name',
            'description': 'The name of the argument.',
            'required': True
        },
        {
            'name': 'argument_description',
            'description': 'The comment of the argument from the program',
            'required': True
        },
        {
            'name': 'expression',
            'description': 'The argument value.',
            'required': True
        },
        {
            'name': 'expression_type',
            'description': 'The type of the argument value.',
            'required': True
        },
        {
            'name': 'output_type',
            'description': 'The intended final type of the argument value.',
            'required': True
        },
    )

    @docval(
        *get_docval(DynamicTable.__init__, 'id', 'columns', 'colnames'),
        {
            'name': 'description',
            'type': str,
            'doc': 'A table to hold the task arguments from the program.',
            'default': 'state type data',
        },
        {
            'name': 'beadl_task_program',
            'type': BEADLTaskProgram,
            'doc': 'the BEADLTaskProgram used',
            'default': None},
        {
            'name': 'populate_from_program',
            'type': bool,
            'doc': 'Boolean to populate from task program.',
            'default': False}
    )
    def __init__(self, **kwargs):
        kwargs['name'] = 'task_arguments'
        beadl_task_program = popargs('beadl_task_program', kwargs)
        populate_from_program = popargs('populate_from_program', kwargs)
        super().__init__(**kwargs)
        self.beadl_task_program = beadl_task_program
        if self.beadl_task_program == None:
            self.populate_from_program = False
        else:
            self.populate_from_program = populate_from_program
        if self.populate_from_program:
            self._populate_from_program()

    def _populate_from_program(self):
        parsed_xml_object = BeadlXMLParser(string=self.beadl_task_program.data)
        element = parsed_xml_object.element(element_name='BeadlArguments')
        parsed_arg_element = parsed_xml_object._parse_protocal_children(element=element)
        beadl_args = parsed_arg_element['BeadlArgument']

        for arg in beadl_args:
            super().add_row(argument_name=arg['name'],argument_description=arg['comment'], expression=arg['expression'],
                            expression_type=arg['expressionType'], output_type=arg['outputType'])
