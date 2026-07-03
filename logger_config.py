import logging
import os

CARPETA_LOGS = os.path.join(os.path.dirname(os.path.abspath(__file__)), "logs")
os.makedirs(CARPETA_LOGS, exist_ok=True)

RUTA_LOG = os.path.join(CARPETA_LOGS, "eventos.log")

logger = logging.getLogger("SoftwareFJ")
logger.setLevel(logging.DEBUG)

if not logger.handlers:
    file_handler = logging.FileHandler(RUTA_LOG, encoding="utf-8")
    file_handler.setLevel(logging.DEBUG)

    formato = logging.Formatter(
        "%(asctime)s | %(levelname)-8s | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )
    file_handler.setFormatter(formato)

    logger.addHandler(file_handler)
