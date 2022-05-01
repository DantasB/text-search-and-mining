from typing import Tuple
from xml.dom.minidom import Document
from vetorial_model.processor.reader.data_reader import DataReader
from vetorial_model.utils.normalizer_utils import Normalize
from vetorial_model.processor.generator.default import DefaultGenerator


class QueriesGenerator(DefaultGenerator):
    """Initialize the QueriesGenerator

    Args:
        file_path (str): The path of the csv file.
        separator (str): The separator of the csv file. Default: ";"
    """

    __COLUMNS = ["NUMBER", "TEXT"]

    def __init__(self, file_path: str, separator: str = ";"):
        super().__init__(file_path, self.__COLUMNS, separator)
        super().setup_generator_logger("QueriesGenerator")

    @staticmethod
    def build_csv_row(reader: DataReader, document: Document) -> Tuple[str, str]:
        """Build the csv row for the query

        Args:
            reader (DataReader): The data reader
            document (Document): The query

        Returns:
            Tuple[str, str]: The last_query_number and the normalized_text
        """

        numbers = reader.get_tag_elements("QueryNumber", document)
        query_number = reader.get_tag_element_value(numbers[-1])

        texts = reader.get_tag_elements("QueryText", document)
        last_text = reader.get_tag_element_value(texts[-1])
        return query_number, Normalize(last_text).normalized_text
