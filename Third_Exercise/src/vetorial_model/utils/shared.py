import math


def calculate_tf_idf(
    number_of_documents: int, number_of_terms: int, document_frequency: int
) -> int:
    """Calculate the tfidf of a word

    Args:
        number_of_documents (int): The number of documents
        number_of_terms (int): The number of terms
        document_frequency (int): The document frequency

    Returns:
        int: The tfidf
    """
    return 1 + math.log(document_frequency) * math.log(
        number_of_documents / number_of_terms
    )
