import csv
import requests
import xml.etree.ElementTree as ET
from collections import defaultdict

path = "/Users/mavaylon/Research/NWB/ndx-structured-behavior/src/pynwb/tests/Foraging_Task.xml"

class BeadlXMLParser():
    def __init__(self, **kwargs):
        # if kwargs['path'] is not None:
        #     self.path = kwargs['path'] # path to xml file
        #     self._xml_object = ET.parse(path)
        #     self._root = self._establish_root()
        # else:
        self._root = ET.fromstring(kwargs['string'])
        self.version = self._beadl_version()
        self._protocal = self._establish_protocal()

    # def _establish_root(self):
    #     """
    #     Helper function to establish root
    #     """
    #     root_object = self._xml_object.getroot()
    #     return root_object

    def _beadl_version(self):
        """
        Return the Beadl version from the xml
        """
        return self._root.attrib

    def _establish_protocal(self):
        """
        Helper function to establish beadl_trial_protocal
        """

        return list(self._root)[0]

    def beadl_trial_protocal_attributes(self):
        """
        Return the name, starting state, and number of trials of the BeadlTrialProtocal
        """
        return self._protocal.attrib

    def element(self, **kwargs):
        """
        Takes in an element from the beadl_trial_protocal level in the xml file,
        e.g BeadlArguments, HardwareSettings, BeadlInputs, BeadlActions, BeadlStates,
        and BeadlStateTransitions.
        """

        element_name = kwargs['element_name']
        element = self._protocal.find(element_name)

        return element

    def _parse_protocal_children(self, **kwargs):
        """
        Takes in an element from the beadl_trial_protocal level in the xml file,
        e.g BeadlArguments, HardwareSettings, BeadlInputs, BeadlActions, BeadlStates,
        and BeadlStateTransitions.

        It will return a dictionary containing a list of either a single dictionary,
        or multiple dictionaries. This is due to the fact that their can be more than
        one child for each element, e.g more than one BeadlStates, and we want to be able
        to store them.
        """
        element = kwargs['element']
        element_dict = defaultdict(list) # it is a list because there can be more than one of each child e.g BeadlStates
        for child in element.iter():
            if len(child.attrib)>0:
                element_dict[child.tag].append(child.attrib)
            else:
                element_dict[child.tag].append(child.text)
        return element_dict

    def display_element(self, element, level=0):
        """
        Takes in an element from the beadl_trial_protocal level in the xml file,
        e.g BeadlArguments, HardwareSettings, BeadlInputs, BeadlActions, BeadlStates,
        and BeadlStateTransitions.

        Workflow for BeadlStates:
        b=BeadlXMLParser(path='...')
        s=b.element(element_name='BeadlStates')

        b.display_element(s)
        """
        self._print_level(element,level)
        for child in list(element):
            self.display_element(child, level+2)

    def _print_level(self, element, level):
        print ('-'*level+element.tag)
        print(' '*(level+(int(len(element.tag)/2)))+'|')
        for item in element.attrib:
            if element.attrib[item] is not None:
                print(' '*(level+(int(len(element.tag)/2)))+'|---'+item+':',element.attrib[item])
            # elif element.find(item) is not None:
            #     print(' '*(level+(int(len(element.tag)/2)))+'|---'+item+':',element.find(item).text)

    def retrieve_state_type(self, state_type):
        states_element = self.element(element_name='BeadlStates').findall('BeadlState')
        for states in states_element:
            if states.attrib['name']==state_type:
                parsed_child = self._parse_protocal_children(element=states)
        return parsed_child
