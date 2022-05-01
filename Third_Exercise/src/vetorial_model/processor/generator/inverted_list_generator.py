from typing import Any, Dict, List
from xml.dom.minidom import Document
from vetorial_model.utils.normalizer_utils import Normalize
from vetorial_model.processor.reader.data_reader import DataReader
from vetorial_model.processor.generator.default import DefaultGenerator


class InvertedListGenerator(DefaultGenerator):
    """Initialize the InvertedListGenerator

    Args:
        file_path (str): The path of the file.
        separator (str): The separator of the csv file. Default: ";"
    """

    __COLUMNS = ["WORD", "DOCUMENTS_LIST"]

    def __init__(self, file_path: str, separator: str = ";"):
        super().__init__(file_path, self.__COLUMNS, separator)
        super().setup_generator_logger("InvertedListGenerator")

    def build_csv_row(self, reader: DataReader, document: Document):
        """Build the csv row for the inverted list

        Args:
            reader (DataReader): The data reader
            document (Document): The inverted list

        Returns:
            List[str]: The list of rows for the csv file
        """
        rows: List[Any] = []
        record_numbers = reader.get_tag_elements("RECORDNUM", document)
        record_num = reader.get_tag_element_value(record_numbers[-1])
        if not record_num:
            return rows

        abstracts = reader.get_tag_elements("ABSTRACT", document)
        abstract = ""
        if len(abstracts) == 0:
            abstracts = reader.get_tag_elements("EXTRACT", document)
            if len(abstracts) == 0:
                return rows

        abstract = reader.get_tag_element_value(abstracts[-1])
        abstract_words = Normalize(abstract).tokenized_text
        for text in abstract_words:
            rows.append(f"{text.strip()}{self.separator}{record_num.strip()}")

        return rows

    def group_by_word(self, rows: list) -> dict:
        """Group the rows by word

        Args:
            rows (list): The rows

        Returns:
            dict: The grouped rows
        """

        grouped_rows: Dict[str, List[str]] = {}
        for row in rows:
            splitted_row = row.split(self.separator)
            word = splitted_row[0]
            if not word:
                continue

            if word not in grouped_rows:
                grouped_rows[word] = []
            grouped_rows[word].append(splitted_row[1])

        return grouped_rows
