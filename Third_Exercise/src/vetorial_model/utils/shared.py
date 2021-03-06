import math


def calculate_tf_idf(
    number_of_documents: int, number_of_terms: int, document_frequency: int
) -> float:
    """Calculate the tfidf of a word

    Args:
        number_of_documents (int): The number of documents
        number_of_terms (int): The number of terms
        document_frequency (int): The document frequency

    Returns:
        float: The tfidf
    """
    if document_frequency == 0:
        return 0

    return (1 + math.log2(document_frequency)) * math.log2(
        number_of_documents / number_of_terms
    )
