import logging

LOGGING_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
logging.basicConfig(format="%(levelname)s:%(message)s", level=logging.INFO)
