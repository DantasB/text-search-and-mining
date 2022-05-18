
from typing import Set


def precision(documents: Set, expected_documents: Set) -> float:
    """ Calculates precision
    
    Args:
        documents (Set): Set of documents
        expected_documents (Set): Set of expected documents
    Returns:
        float: Precision
    """
    return len(documents & expected_documents) / len(documents) * 100 if len(documents) > 0 else 0

def f1_score(precision: float, recall: float) -> float:
    """ Calculates F1 score
    
    Args:
        precision (float): Precision
        recall (float): Recall
    Returns:
        float: F1 score
    """
    return 2 * precision * recall / (precision + recall) * 100 if (precision + recall) > 0 else 0

def recall (documents: Set, expected_documents: Set) -> float:
    """ Calculates recall
    
    Args:
        documents (Set): Set of documents
        expected_documents (Set): Set of expected documents
    Returns:
        float: Recall
    """
    return len(documents & expected_documents) / len(expected_documents) * 100 if len(expected_documents) > 0 else 0
