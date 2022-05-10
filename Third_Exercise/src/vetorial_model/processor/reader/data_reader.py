from typing import Optional
from xml.dom.minidom import Document, Element, parse
from vetorial_model.processor.reader.default import DefaultReader


class DataReader(DefaultReader):
    """Initialize the DataReader

    Args:
        file_path (str): The path of the xml file.
    """

    def __init__(self, file_path: Optional[str] = None):
        super().__init__(file_path)
        super().setup_reader_logger("DataReader")

    def __read_xml_doc(self) -> Document:
        """Read the xml file

        Returns:
            Document: The xml file
        """
        self.logger.info(f"Reading xml file {self.file_path}")

        if not self.file_path:
            raise Exception("Xml file not found")

        return parse(self.file_path)

    def get_tag_elements(self, tag_name: str, xml_doc: Optional[Document] = None):
        """Get the tag elements

        Args:
            tag_name (str): The name of the tag
            xml_doc (Document): The xml file

        Returns:
            list: The tag elements
        """
        print("\n")
        self.logger.info(f"Reading tag elements {tag_name}")
        if xml_doc is None and not self.file_path:
            raise Exception("Xml file not found")

        document = xml_doc or self.__read_xml_doc()
        tag_elements = document.getElementsByTagName(tag_name)
        self.logger.info(f"Found {len(tag_elements)} tag elements")
        return tag_elements

    def get_tag_element_value(self, tag_element):
        """Get the tag element value

        Args:
            tag_element (xml.dom.minidom.Element): The tag element

        Returns:
            str: The tag element value
        """
        self.logger.info(f"Reading tag element value {tag_element.nodeName}")
        if tag_element.firstChild is None:
            return None
        return tag_element.firstChild.data

    def get_tag_element_attribute_value(
        self, tag_element: Element, attribute_name: str
    ):
        """Get the tag element attribute value

        Args:
            tag_element (Element): The tag element
            attribute_name (str): The name of the attribute

        Returns:
            str: The tag element attribute value
        """
        self.logger.info(
            f"Reading tag element attribute value {tag_element.nodeName} {attribute_name}"
        )
        return tag_element.getAttribute(attribute_name)
