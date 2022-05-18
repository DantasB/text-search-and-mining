import ast
from typing import Dict, Set
import pandas as pd

from vetorial_model.utils.logger_utils import get_logger_with_date_output


class Validator:
    def __init__(self, results_path: str, expected_results_path: str):
        self.results_path = results_path
        self.results = self.__read(results_path)
        self.expected_results_path = expected_results_path
        self.expected_results = self.__read(expected_results_path)
        self.output_path = "Avalia/results.csv"
        self.logger = get_logger_with_date_output("Validator")

    @staticmethod
    def __read(path: str):
        results = pd.read_csv(path, sep=";", header=0)
        return results

    def change_expected_results_format(self):
        expected_results = pd.DataFrame(columns=["Query", "Ranking"])

        for query_number in self.expected_results["NUMBER"].unique():
            query_df = self.expected_results.loc[
                self.expected_results["NUMBER"] == query_number
            ].iloc[:, 1:]
            result_tuples = []
            rank = 0
            for doc, score in query_df.sort_values(
                "DOCVOTES", ascending=False
            ).itertuples(False, None):
                rank += 1
                result_tuples.append((rank, doc, score))

            expected_results = pd.concat(
                [
                    expected_results,
                    pd.DataFrame(
                        [(query_number, result_tuples)],
                        columns=["Query", "Ranking"],
                    ),
                ]
            )

        self.expected_results = expected_results

    def filter_documents(self, results_df:pd.DataFrame, threshold:float, evaluate:bool) -> Set:
        """ Filters documents based on threshold 

        Args:
            results_df (pd.DataFrame): Dataframe with documents
            threshold (float): Threshold to filter documents
            evaluate (bool): Parses the string list to a list of values
        Returns:
            Set: Set of documents filtered
        """

        filtered_documents = set()
        for result in results_df["Ranking"].values:
            if evaluate:
                result = ast.literal_eval(result)
            for _, document, score in result:
                if score > threshold:
                    filtered_documents.add(int(document))
        return filtered_documents

    def save_results(self, results: Dict[int, Dict[str, float]]):
        self.logger.info("Saving results")
        df = pd.DataFrame(columns=["Query", "Precision", "Recall", "F1"])
        for query, result in results.items():
            df = df.append(
                {
                    "Query": query,
                    "Precision": result["Precision"],
                    "Recall": result["Recall"],
                    "F1": result["F1"],
                },
                ignore_index=True,
            )

        df.to_csv(self.results_path, sep=";", index=False)
        self.logger.info("Results saved")
    
    def validate(self):
        self.change_expected_results_format()
        self.logger.info("Comparing results")
        results = {}

        for query in self.expected_results["Query"].unique():
            results[query] = {}
            results_df = self.results.loc[self.results["Query"] == query]
            expected_results_df = self.expected_results.loc[
                self.expected_results["Query"] == query
            ]
            self.logger.info(f"Comparing query {query}")
            
            documents = self.filter_documents(results_df, threshold=0.0001, evaluate=True)
            expected_documents = self.filter_documents(expected_results_df, threshold=0, evaluate=False)

            results[query]["Precision"] = len(documents.intersection(expected_documents)) / len(documents) * 100 if len(documents) > 0 else 0

            results[query]["Recall"] = len(documents.intersection(expected_documents)) / len(expected_documents) * 100 if len(expected_documents) > 0 else 0

            results[query]["F1"] = (
                2 * results[query]["Precision"] * results[query]["Recall"]
            ) / (results[query]["Precision"] + results[query]["Recall"]) if (
                results[query]["Precision"] + results[query]["Recall"]
            ) > 0 else 0

        self.save_results(results)
