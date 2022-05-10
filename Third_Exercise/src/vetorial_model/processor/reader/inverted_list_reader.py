from typing import List
from vetorial_model.processor.reader.data_reader import DataReader


class InvertedListReader(DataReader):
    """Initialize the InvertedListReader

    Args:
        file_path (str): The path of the file.
    """

    def __init__(self, files: List[str]):
        super().__init__()
        super().setup_reader_logger("InvertedListReader")
        self.files = files
