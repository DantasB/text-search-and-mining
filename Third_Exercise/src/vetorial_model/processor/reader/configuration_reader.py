from typing import List
from vetorial_model.processor.reader.default import DefaultReader


class ConfigurationReader(DefaultReader):
    """Initialize the ConfigurationReader

    Args:
        file_path (str): The path of the configuration file.
    """

    def __init__(self, file_path):
        super().__init__(file_path)
        super().setup_reader_logger("ConfigurationReader")
        self.queries = self.get_configuration_attribute("CONSULTAS")
        self.read = self.get_configuration_attribute("LEIA")
        self.expected = self.get_configuration_attribute("ESPERADOS")
        self.write = self.get_configuration_attribute("ESCREVA")
        self.model = self.get_configuration_attribute("MODELO")
        self.results = self.get_configuration_attribute("RESULTADOS")
        self.stemmer = self.get_configuration_attribute("STEMMER")

    def define_stemmer(self, stemmer: str) -> bool:
        """Define if the stemmer is used

        Args:
            stemmer (str): The name of the stemmer

        Returns:
            bool: True if the stemmer is used
        """
        if stemmer == "STEMMER":
            return True
        elif stemmer == "NOSTEMMER":
            return False
        self.logger.warning(
            "The stemmer name is not defined. The default stemmer is used."
        )
        return False

    def get_configuration_attribute(self, attribute_name: str) -> List[str]:
        """Get the value of the attribute

        Args:
            attribute_name (str): The name of the attribute

        Returns:
            str: The value of the attribute
        """
        values = []
        self.logger.info(f"Reading configuration attribute {attribute_name}")
        with self.read_file() as configuration_attributes:
            for configuration_attribute in configuration_attributes:
                configuration_attribute = configuration_attribute.split("=")
                if len(configuration_attribute) == 1 and attribute_name == "STEMMER":
                    return configuration_attribute[0].rstrip("\n")
                if configuration_attribute[0] == attribute_name:
                    attribute_value = configuration_attribute[1]
                    self.logger.info(
                        f"Found configuration attribute: {attribute_name}. Value: {attribute_value}"
                    )
                    values.append(attribute_value.rstrip("\n"))
        if len(values) == 0:
            self.logger.warning(
                f"Could not find configuration attribute: {attribute_name}"
            )

        return values
