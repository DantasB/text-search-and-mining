import re
import unicodedata
import nltk

nltk.download("stopwords")
nltk.download("punkt")


class Normalize:
    def __init__(self, text: str):
        """Initialize the Normalize class

        Args:
            text (str): Text to normalize
        """
        self.text = text
        self.normalized_text = self.normalize(text)
        self.normalized_text_size = len(self.normalized_text)
        self.tokenized_text = self.__tokenize()

    @staticmethod
    def __remove_accent(text: str) -> str:
        """Remove accent from text

        Args:
            text (str): Text to remove accent

        Returns:
            str: Text without accent
        """ """ Remove accent from text """
        text = (
            unicodedata.normalize("NFKD", text)
            .encode("ASCII", "ignore")
            .decode("utf-8", "ignore")
        )
        return text

    @staticmethod
    def __treat_text(text: str) -> str:
        """Remove \t \n \r from text

        Args:
            text (str): Text to treat

        Returns:
            str: Text without \t \n \r
        """
        text = text.replace("\t", " ")
        text = text.replace("\n", " ")
        text = text.replace("\r", " ")
        return text

    @staticmethod
    def __remove_semicolon(text):
        """Remove semicolon from text

        Args:
            text (str): Text to remove semicolon

        Returns:
            str: Text without semicolon
        """
        text = text.replace(";", "")
        return text

    @staticmethod
    def __replace_multiple_space_by_one_regex(text):
        """Replace multiple space by one regex

        Args:
            text (str): Text to replace multiple space by one regex

        Returns:
            str: Text without multiple space
        """
        text = re.sub(r"\s+", " ", text)
        return text

    @staticmethod
    def __remove_quotes(text):
        """Remove quotes from text

        Args:
            text (str): Text to remove quotes

        Returns:
            str: Text without quotes
        """
        text = text.replace('"', "")
        text = text.replace("'", "")
        return text

    @staticmethod
    def __remove_parenthesis(text):
        """Remove parenthesis from text

        Args:
            text (str): Text to remove parenthesis

        Returns:
            str: Text without parenthesis
        """
        text = text.replace("(", "")
        text = text.replace(")", "")
        return text

    @staticmethod
    def __remove_punctuation(text) -> str:
        """Remove punctuation from text

        Args:
            text (str): Text to remove punctuation

        Returns:
            str: Text without punctuation
        """
        text = text.replace(".", "")
        text = text.replace(",", "")
        text = text.replace("!", "")
        text = text.replace("?", "")
        text = text.replace("-", "")
        text = text.replace("/", "")
        text = text.replace("(", "")
        text = text.replace(")", "")
        return text

    @staticmethod
    def __remove_keys_brackets(text):
        """Remove keys brackets from text

        Args:
            text (str): Text to remove keys and brackets

        Returns:
            str: Text without keys and brackets
        """
        text = text.replace("{", "")
        text = text.replace("}", "")
        return text

    @staticmethod
    def __remove_square_brackets(text):
        """Remove square brackets from text

        Args:
            text (str): Text to remove square brackets

        Returns:
            str: Text without square brackets
        """
        text = text.replace("[", "")
        text = text.replace("]", "")
        return text

    def normalize(self, text):
        """Normalize text

        Args:
            text (str): Text to normalize

        Returns:
            str: Normalized text
        """
        text = self.__remove_accent(text)
        text = self.__remove_semicolon(text)
        text = self.__treat_text(text)
        text = self.__replace_multiple_space_by_one_regex(text)
        text = self.__remove_quotes(text)
        text = self.__remove_parenthesis(text)
        text = self.__remove_keys_brackets(text)
        text = self.__remove_square_brackets(text)
        text = self.__remove_punctuation(text)
        return text.upper()

    def calculate_number_of_votes(self) -> int:
        """Any number differente of zero is a vote

        Returns:
            int: Number of votes
        """
        return self.normalized_text_size - (len(self.normalized_text.split("0")) - 1)

    def __tokenize(self) -> list:
        """Tokenize text

        Returns:
            list: List of tokens
        """
        stop_words = [word.upper() for word in nltk.corpus.stopwords.words("english")]
        return [
            word
            for word in nltk.word_tokenize(self.normalized_text)
            if word not in stop_words
        ]
