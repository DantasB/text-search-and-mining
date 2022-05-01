from contextlib import contextmanager
from typing import Optional
from vetorial_model.utils.logger_utils import get_logger_with_date_output


class DefaultReader:
    """Initialize the DefaultReader

    Args:
        file_path (str): The path of the file.
    """

    def __init__(self, file_path: Optional[str] = None):
        self.file_path = file_path
        self.setup_reader_logger("DefaultReader")

    @contextmanager
    def read_file(
        self, archive: Optional[str] = None, read_from_file_path: bool = True
    ):
        """Read the file

        Args:
            archive (File): The file
            read_from_file_path (bool): If the file path should be used
        Yields:
            TextIOWrapper: The file
        """
        if read_from_file_path and self.file_path is not None:
            with open(self.file_path, "r", encoding="utf-8") as file:
                yield file
        elif not read_from_file_path and archive is not None:
            with open(archive, "r", encoding="utf-8") as file:
                yield file
        elif read_from_file_path and self.file_path is None:
            raise ValueError("The file_path is not set. Please set the file_path.")
        else:
            raise ValueError("The file is not set")

    def setup_reader_logger(self, logger_name: str):
        """Setup the logger

        Args:
            logger_name (str): The name of the logger
        """

        self.logger = get_logger_with_date_output(logger_name)

    def set_file_path(self, file_path: str):
        """Set the file path

        Args:
            file_path (str): The file path
        """

        self.file_path = file_path
