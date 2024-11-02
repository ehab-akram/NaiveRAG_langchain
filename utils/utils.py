import json
import logging
import os
from pathlib import Path

logger = logging.getLogger(__name__)


def setup_logging():
    log_format = '%(asctime)s - %(filename)s - %(levelname)s - %(message)s'
    Stream_format = '%(name)-12s: %(levelname)-8s %(message)s'
    logFile_path = Path('..\\..\\logs\\logs.log').resolve()
    level = logging.INFO

    # check if the file not exists to create one
    os.makedirs(os.path.dirname(logFile_path), exist_ok=True)

    # init the logger
    logging.basicConfig(
        format=log_format,
        filename=logFile_path,
        filemode='a',
        level=level
    )

    # Add the logs to the output Console
    console = logging.StreamHandler()

    console.setLevel(level)
    console.setFormatter(logging.Formatter(Stream_format))

    logging.getLogger().addHandler(console)

    logging.info("Logging is set up")


def ConvertorFileWrite(filepath, text):
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(text)
        logger.info(f"File Converted and Saved {filepath}")


def load_settings(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        configr = json.load(f)
    logger.info(f"The Config Loaded Successfully")
    return configr
