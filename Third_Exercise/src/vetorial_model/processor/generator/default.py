from typing import Dict, List

from vetorial_model.utils.logger_utils import get_logger_with_date_output


class DefaultGenerator:
    """Initialize the DefaultGenerator

    Args:
        file_path (str): The path of the csv file.
        columns (List[str]): The columns of the csv file.
        separator (str): The separator of the csv file. Default: ";"
    """

    def __init__(self, file_path: str, columns: List[str], separator: str = ";"):
        self.setup_generator_logger("DefaultGenerator")
        self.separator = separator
        self.file_path = file_path
        self.columns = separator.join(columns)
        self.__write_csv_header_to_file_path()

    def __write_csv_header_to_file_path(self):
        """Write the csv header to the file path"""
        self.logger.info(f"Writing csv header to file {self.file_path}")
        with open(self.file_path, "w+", encoding="utf-8") as file:
            file.write(self.columns)
            file.write("\n")

    def write_list_to_file_path(self, csv_rows: List[str]):
        """Write the csv rows as list to the file path

        Args:
            csv_rows (List[str]): The csv rows.
        """
        self.logger.info(f"Writing {len(csv_rows)} csv rows to file {self.file_path}")
        with open(self.file_path, "a", encoding="utf-8") as file:
            file.write("\n".join(csv_rows))

    def write_dictionary_to_file_path(self, csv_rows: Dict[str, List[str]]):
        """Write the csv rows as dictionary to the file path

        Args:
            csv_rows (Dict[str, List[str]]): The csv rows.
        """
        self.logger.info(f"Writing {len(csv_rows)} csv rows to file {self.file_path}")
        with open(self.file_path, "a", encoding="utf-8") as file:
            file.write(
                "\n".join(
                    f"{key}{self.separator}{value}" for key, value in csv_rows.items()
                )
            )

    def setup_generator_logger(self, class_name: str):
        """Setup the logger for the class

        Args:
            class_name (str): The class name
        """
        self.logger = get_logger_with_date_output(class_name)

    def setup_generator_logger(self, logger_name: str):
        """Setup the logger

        Args:
            logger_name (str): The name of the logger
        """

        self.logger = get_logger_with_date_output(logger_name)
