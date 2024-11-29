import logging
import sys


def configure_logging(level: int):
    logger = logging.getLogger()
    logger.setLevel(level)

    # Формат логирования
    formatter = logging.Formatter("%(asctime)s [%(levelname)s] %(message)s")

    # Консольный логгер
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    # Лог в файл
    file_handler = logging.FileHandler("../../app.log")
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    return logger
