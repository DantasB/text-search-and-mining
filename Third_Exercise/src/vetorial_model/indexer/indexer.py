import ast
from collections import Counter
from typing import Dict
import pandas as pd
from vetorial_model.utils.logger_utils import get_logger_with_date_output
from vetorial_model.utils.shared import calculate_tf_idf


class Indexer:
    def __init__(
        self, inverted_list_file_path: str, last_document: str, save_path: str
    ):
        self.inverted_list_file_path = inverted_list_file_path
        self.save_path = save_path
        self.last_document = int(last_document.strip())
        self.logger = get_logger_with_date_output("Indexer")
        self.words_table = self.__read_words_table(inverted_list_file_path)
        self.list_of_documents = self.__get_list_of_documents()
        self.total_of_terms_on_documents = (
            self.__calculate_total_of_terms_on_documents()
        )

    def __read_words_table(self, file_path: str) -> pd.DataFrame:
        """Read the words table from the file path

        Args:
            file_path (str): The file path

        Returns:
            pd.DataFrame: The words table
        """
        self.logger.info("Reading words table")
        words_table = pd.read_csv(file_path, sep=";", encoding="utf_8")
        words_table = self.__filter_dataframe(words_table, 2)
        self.logger.info("Words table read")
        return words_table

    def __get_list_of_documents(self) -> list:
        """Get the list of documents

        Returns:
            list: The list of documents
        """
        self.logger.info("Getting list of documents")
        list_of_documents = []
        for _, row in self.words_table.iterrows():
            documents = ast.literal_eval(row["DOCUMENTS_LIST"])
            list_of_documents.extend(documents)

        list_of_documents = list(set(list_of_documents))

        self.logger.info("List of documents retrieved")
        return list_of_documents

    def __filter_dataframe(self, dataframe: pd.DataFrame, size: int) -> pd.DataFrame:
        """Given a size, drop every line that the word size is lower or equal than this value.

        Args:
            dataframe (pd.DataFrame): The dataframe to be filtered
            size (int): The size to be filtered

        Returns:
            pd.Dataframe: The filtered dataframe
        """
        self.logger.info("Filtering dataframe")
        dataframe = dataframe[dataframe.WORD.str.len() > size]
        dataframe = dataframe.reset_index(drop=True)
        self.logger.info("Dataframe filtered")

        return dataframe

    def __calculate_total_of_terms_on_documents(self) -> Dict[str, int]:
        """Calculate the total of terms on documents

        Returns:
            Dict[str, int]: The total of terms on documents
        """
        self.logger.info("Calculating total of terms on documents")
        total_of_terms_on_documents = {}
        for document in self.list_of_documents:
            total_of_terms_on_documents[document] = len(
                self.words_table[
                    self.words_table["DOCUMENTS_LIST"].str.contains(document)
                ]
            )

        self.logger.info("Total of terms on documents calculated")
        return total_of_terms_on_documents

    def calculate_dataframe_tfidf(self) -> pd.DataFrame:
        """Calculate the tfidf of the dataframe

        Returns:
            pandas.DataFrame: The dataframe with the tfidf
        """

        dataframe = self.words_table.join(
            pd.DataFrame(
                0.0,
                index=self.words_table.index,
                columns=self.list_of_documents,
            )
        )

        self.logger.info("Calculating tfidf")
        for index, row in dataframe.iterrows():
            documents = ast.literal_eval(row["DOCUMENTS_LIST"])
            word_frequence_on_document = Counter(documents)
            for document in documents:
                dataframe.at[index, document] = calculate_tf_idf(
                    self.last_document,
                    len(set(documents)),
                    word_frequence_on_document[document],
                )

        self.logger.info("Tfidf calculated")
        dataframe = dataframe.drop(["DOCUMENTS_LIST"], axis=1)
        return dataframe

    def write_dataframe_to_file_path(self, dataframe: pd.DataFrame):
        """Write the dataframe to the file path

        Args:
            dataframe (pandas.DataFrame): The dataframe to be written
        """
        self.logger.info("Writing model to file path")
        dataframe.to_csv(self.save_path, index=False, sep=";", encoding="utf_8")
        self.list_of_documents = dataframe.columns.tolist()[1:]
        self.logger.info("Model written to file path")
