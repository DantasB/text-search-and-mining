from typing import List
from xml.dom.minidom import Document
from vetorial_model.processor.reader.data_reader import DataReader
from vetorial_model.utils.normalizer_utils import Normalize
from vetorial_model.processor.generator.default import DefaultGenerator


class ExpectedGenerator(DefaultGenerator):
    """Initialize the ExpectedGenerator

    Args:
        file_path (str): The path of the csv file.
        separator (str): The separator of the csv file. Default: ";"
    """

    __COLUMNS = ["NUMBER", "DOCNUMBER", "DOCVOTES"]

    def __init__(self, file_path: str, separator: str = ";"):
        super().__init__(file_path, self.__COLUMNS, separator)
        super().setup_generator_logger("ExpectedGenerator")

    def build_csv_row(
        self,
        reader: DataReader,
        document: Document,
        query_number: str,
    ):
        """Build the csv row for the waited query

        Args:
            reader (data_reader.DataReader): The data reader
            document (Document): The query
            query_number (str): The query number

        """
        rows = []
        records = reader.get_tag_elements("Records", document)
        for record in records:
            items = reader.get_tag_elements("Item", record)
            for item in items:
                doc_number = reader.get_tag_element_value(item)
                doc_votes = Normalize(
                    reader.get_tag_element_attribute_value(item, "score")
                ).calculate_number_of_votes()
                rows.append(
                    f"{query_number}{self.separator}{doc_number}{self.separator}{doc_votes}"
                )
        return rows
