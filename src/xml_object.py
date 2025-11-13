import logging
from dataclasses import dataclass
import xml.etree.ElementTree as ET

logger = logging.getLogger(__name__)

@dataclass
class XMLObject:
    """
    Object representation of an XML object. Contains the element and string representations of the object.
    Elements are represented using ElementTree.
    """
    element: ET.Element     # Represents the element representation of an XML object using ElementTree
    string: str             # Represents the string representation of an XML object

    def __init__(self, data: str):
        self.element = XMLObject.toTreeElement(data)
        self.string = data

    @staticmethod
    def print_element(element: ET.Element) -> None:
        """
        Print the element and its children.
        """
        logger.debug(ET.tostring(element).decode())

    @staticmethod
    def remove_bom(xml_string: str) -> str:
        """
        Remove the Byte Order Mark (BOM) from an XML string.
        """
        return xml_string[3:]
    
    @staticmethod
    def toTreeElement(xml_string: str) -> ET.Element:
        """
        Parse an XML string and return the root element of the tree.
        """
        return ET.fromstring(xml_string)

    def get_string(self) -> str:
        """
        Get the string representation of the XML object.
        """
        return self.string.encode('latin1').decode('utf-8') if self.string else None
    
    def get_tree_element(self) -> ET.Element:
        """
        Get the tree element representation of the XML object.
        """
        return self.element
    
    def find_first_element_by_name(self, element_name: str) -> 'XMLObject':
        """
        Find the first element with the given name in an XML string.
        If Parsing Error occurs, print the error and the first 100 characters of the XML.

        :param xml_string: XML string to search in.
        :param element_name: Name of the element to find.

        :return: XMLObject representing the first element with the given name.
        """
        try:
            element = self.get_tree_element().find(f".//{element_name}")
            return XMLObject(element, element.text) if element is not None else None
        except ET.ParseError as e:
            logger.error(f"XML Parsing Error: {e}")
            logger.error(f"First 100 characters of XML: {repr(self.get_tree_element()[:100])}")
            raise
    
    def find_elements_by_name(self , element_name: str) -> list['XMLObject']:
        """
        Find all elements with a given name in an XML string.
        If Parsing Error occurs, print the error and the first 100 characters of the XML.

        :param xml_string: XML string to search in.
        :param element_name: Name of the elements to find.

        :return: List of XMLObjects representing the elements with the given name.
        """
        try:
            element = self.get_tree_element().findall(f".//{element_name}")
            return [XMLObject(e, e.text) for e in element]
        except ET.ParseError as e:
            logger.error(f"XML Parsing Error: {e}")
            logger.error(f"First 100 characters of XML: {repr(self.get_tree_element()[:100])}")
            raise