from typing import List
from vetorial_model.indexer.indexer import Indexer
from vetorial_model.processor.generator import (
    inverted_list_generator as ilg,
    queries_generator as qg,
    expected_generator as eg,
)

from vetorial_model.processor.reader import (
    configuration_reader,
    data_reader,
    inverted_list_reader,
)
from vetorial_model.search_engine.engine import SearchEngine
from vetorial_model.validator.validator import Validator

CONSULT_PROCESSOR_CONFIG_FILE = "./Configs/PC.CFG"
INVERT_LIST_CONFIG_FILE = "./Configs/GLI.CFG"
INDEXER_CONFIG_FILE = "./Configs/INDEX.CFG"
BUSCA_CONFIG_FILE = "./Configs/BUSCA.CFG"


def generate_consultas_and_esperados_data():
    """Generate the consultas and esperados data"""

    queries_normalized_data: List[str] = []
    waited_queries: List[str] = []

    configuration = configuration_reader.ConfigurationReader(
        CONSULT_PROCESSOR_CONFIG_FILE
    )
    data = data_reader.DataReader(configuration.read[0])

    queries_generator = qg.QueriesGenerator(configuration.queries[0])
    expected_generator = eg.ExpectedGenerator(configuration.expected[0])

    queries = data.get_tag_elements("QUERY")
    for query in queries:
        last_query_number, query_text = queries_generator.build_csv_row(data, query)
        queries_normalized_data.append(f"{last_query_number};{query_text}")
        waited_queries += expected_generator.build_csv_row(
            data, query, last_query_number
        )

    queries_generator.write_list_to_file_path(queries_normalized_data)

    expected_generator.write_list_to_file_path(waited_queries)


def generate_inverted_list_data():
    """Generate the inverted list data"""
    inverted_list_configuration = configuration_reader.ConfigurationReader(
        INVERT_LIST_CONFIG_FILE
    )

    generator = ilg.InvertedListGenerator(
        inverted_list_configuration.write[0], inverted_list_configuration.stemmer
    )
    reader = inverted_list_reader.InvertedListReader(inverted_list_configuration.read)
    inverted_rows = []
    for file in reader.files:
        reader.set_file_path(file)
        records = reader.get_tag_elements("RECORD")
        for record in records:
            inverted_rows += generator.build_csv_row(reader, record)

    generator.write_dictionary_to_file_path(generator.group_by_word(inverted_rows))
    return generator.last_document, inverted_list_configuration.stemmer


def generate_indexer(last_document: str, stemmer: bool):
    """Generate the model"""
    indexer_configuration = configuration_reader.ConfigurationReader(
        INDEXER_CONFIG_FILE
    )

    indexer = Indexer(
        stemmer,
        indexer_configuration.read[0],
        last_document,
        indexer_configuration.write[0],
    )
    terms_dataframe = indexer.calculate_dataframe_tfidf()
    indexer.write_dataframe_to_file_path(terms_dataframe)
    return indexer.list_of_documents


def search_documents(documents_list: List[str], stemmer: bool):
    """Search documents"""
    search_configuration = configuration_reader.ConfigurationReader(BUSCA_CONFIG_FILE)

    search_engine = SearchEngine(documents_list)
    if stemmer:
        model_path = search_configuration.model[0].replace(".csv", "_stemmer.csv")
        results_path = search_configuration.results[0].replace(".csv", "_stemmer.csv")
    else:
        model_path = search_configuration.model[0].replace(".csv", "_nostemmer.csv")
        results_path = search_configuration.results[0].replace(".csv", "_nostemmer.csv")

    search_engine.read_tf_idf_table_and_generate_term_value_dictionary(model_path)
    search_engine.read_queries_and_generate_query_token_dictionary(
        search_configuration.queries[0]
    )

    result = search_engine.search_documents()
    search_engine.write_search_result(result, results_path)


if __name__ == "__main__":
    # generate_consultas_and_esperados_data()
    # number_of_documents, stemmer = generate_inverted_list_data()
    # list_of_documents = generate_indexer(number_of_documents, stemmer)
    # search_documents(list_of_documents, stemmer)

    validator = Validator(
        results_path="./Results/busca_stemmer.csv",
        expected_results_path="./Results/esperados.csv",
    )

    validator.validate()
