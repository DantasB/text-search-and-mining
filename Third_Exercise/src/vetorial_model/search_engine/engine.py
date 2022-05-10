
from vetorial_model.utils.logger_utils import get_logger_with_date_output


class SearchEngine:
    def __init__(self):
        self.index = {}
        self.logger = get_logger_with_date_output("SearchEngine")
    
    def calculate_similarity_between_query_and_document(self, query: str, document: str) -> float:
        """Calculate the similarity between the query and the document

        Args:
            query (str): The query
            document (str): The document

        Returns:
            float: The similarity
        """
        query_words = query.split()
        document_words = document.split()
        query_words_set = set(query_words)
        document_words_set = set(document_words)
        intersection_size = len(query_words_set.intersection(document_words_set))
        union_size = len(query_words_set.union(document_words_set))
        return intersection_size / union_size