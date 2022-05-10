from vetorial_model.utils.logger_utils import get_logger_with_date_output
import pandas as pd

from vetorial_model.utils.shared import calculate_tf_idf


class Indexer:
    def __init__(
        self, inverted_list_file_path: str, last_document: str, save_path: str
    ):
        self.inverted_list_file_path = inverted_list_file_path
        self.save_path = save_path
        self.last_document = last_document
        self.list_of_documents = []
        self.logger = get_logger_with_date_output("Indexer")
        self.words_table = self.__read_words_table(inverted_list_file_path)
    
    def __read_words_table(self, file_path: str) -> pd.DataFrame:
        """Read the words table from the file path

        Args:
            file_path (str): The file path

        Returns:
            pd.DataFrame: The words table
        """
        self.logger.debug("Reading words table")
        words_table = pd.read_csv(file_path, sep=";", encoding="utf_8")
        self.logger.debug("Words table read")
        return words_table

    def calculate_dataframe_tfidf(self) -> pd.DataFrame:
        """Calculate the tfidf of the dataframe

        Returns:
            pandas.DataFrame: The dataframe with the tfidf
        """

        dataframe = self.words_table.join(
            pd.DataFrame(
                0.0,
                index=self.words_table.index,
                columns=range(1, int(self.last_document) + 1),
            )
        )

        trash_words = []

        self.logger.debug("Calculating tfidf")
        for index in dataframe.index:
            word = dataframe.iloc[index]["WORD"]
            if len(str(word)) < 2:
                trash_words.append(index)

            documents = (
                dataframe.iloc[index]["DOCUMENTS_LIST"][1:-1]
                .strip()
                .replace("'", "")
                .split(",")
            )
            distinct_documents = []
            for document in documents:
                if not (document in distinct_documents):
                    distinct_documents.append(document)

            document_terms = len(distinct_documents)

            for document in distinct_documents:
                freq_doc = documents.count(document)
                dataframe.iat[int(index), int(document) + 1] = calculate_tf_idf(
                    freq_doc, int(self.last_document), document_terms
                )

        dataframe = dataframe.drop(trash_words, axis=0)
        dataframe = dataframe.drop(["DOCUMENTS_LIST"], axis=1)
        self.logger.debug("Tfidf calculated")
        return dataframe

    def write_dataframe_to_file_path(self, dataframe: pd.DataFrame):
        """Write the dataframe to the file path

        Args:
            dataframe (pandas.DataFrame): The dataframe to be written
        """
        self.logger.debug("Writing dataframe to file path")
        dataframe.to_csv(self.save_path, index=False, sep=";", encoding="utf_8")
        self.list_of_documents = dataframe.columns.tolist()[1:]
        self.logger.debug("Dataframe written to file path")
