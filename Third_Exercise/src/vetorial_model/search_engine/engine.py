from typing import List
from numpy import matrix
import pandas as pd
from vetorial_model.utils.logger_utils import get_logger_with_date_output
from vetorial_model.utils.normalizer_utils import Normalize


class SearchEngine:
    def __init__(self, documents_list:List[str]):
        self.index = {}
        self.logger = get_logger_with_date_output("SearchEngine")
        self.documents_list = documents_list
        
    def read_tf_idf_table_and_generate_term_value_dictionary(self, file_path: str) -> dict:
        """Read the tfidf table and generate the term value dictionary

        Args:
            file_path (str): The file path

        Returns:
            dict: The term value dictionary
        """
        self.logger.debug("Reading tfidf table")

        term_value_dictionary = {}
        with open(file_path, "r", encoding="utf_8") as file:
            lines = file.readlines()[1:]
            for line in lines:
                line = line.strip()
                term, *tfidf = line.split(";")
                term_value_dictionary[term] = list(map(float,tfidf))
        self.logger.debug("Tfidf table read")
        self.term_value_dictionary = term_value_dictionary
        return term_value_dictionary

    def read_queries_and_generate_query_token_dictionary(self, file_path: str) -> dict:
        """Read the queries and generate the query token dictionary

        Args:
            file_path (str): The file path  
        Returns:
            dict: The query token dictionary
        """
        self.logger.debug("Reading queries")
        query_token_dictionary = {}
        with open(file_path, "r", encoding="utf_8") as file:
            lines = file.readlines()[1:]
            for line in lines:
                query, text = line.split(";")
                query_token_dictionary[query] = Normalize(text).tokenized_text
        self.logger.debug("Queries read")
        self.query_token_dictionary = query_token_dictionary
        return query_token_dictionary
    
    def calculate_similarity_between(self, tokens: List[str], index: int) -> float:
        """Calculate the similarity between the tokens and the document

        Args:
            tokens (List[str]): The tokens
            index (int): The index

        Returns:
            float: The similarity
        """
        self.logger.debug("Calculating similarity between tokens and document")
        similarity = 0
        for token in tokens:
            if token in self.term_value_dictionary:
                similarity += self.term_value_dictionary[token][index]
        self.logger.debug("Similarity calculated")

        D = 0
        for word in self.term_value_dictionary:
            D += self.term_value_dictionary[word][index] ** 2
        
        if D == 0:
            return 0
        return similarity / D

    def search_documents(self) -> dict:
        """Search the query token dictionary

        Returns:
            dict: The search result
        """
        self.logger.debug("Searching")
        search_result = {}
        for query, tokens in self.query_token_dictionary.items():
            search_result[query] = []
            for index in range(len(self.documents_list)):
                search_result[query].append(
                    [0,
                     self.documents_list[index],
                     self.calculate_similarity_between(tokens, index)]
                )
            
            self.logger.debug("Search finished")
            search_result[query].sort(key=lambda x: x[2], reverse=True)
            for i in range(len(search_result[query])):
                search_result[query][i][0] = i + 1
            

        return search_result

    def write_search_result(self, search_result: dict, file_path: str):
        """Write the search result to the file

        Args:
            search_result (dict): The search result
            file_path (str): The file path
        """
        self.logger.debug("Writing search result")
        with open(file_path, "w", encoding="utf_8") as file:
            file.write("Query;Ranking;\n")
            for query, results in search_result.items():
                file.write(f"{query};{results[query]}\n")