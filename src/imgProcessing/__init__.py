import logging
from .Effects._BaseEffect import BaseImageProcessor
from .Effects.diceify import Diceify
# from .Effects.dither    import Dither  # you’ll need to refactor `dither.py` into a function


__all__ = ["Diceify", "BaseImageProcessor"]

# ——— Logging settings ———————————————
SETTINGS = {
    "LOG_LEVEL"   : logging.INFO,
    "LOG_TO_FILE" : True,
    "LOG_FILE_PATH": "process.log",
    "DEMO_LOGS"   : False,
}

class EmojiFormatter(logging.Formatter):
    EMOJIS = {
        "DEBUG"   : "🐛",
        "INFO"    : "ℹ️",
        "WARNING" : "⚠️",
        "ERROR"   : "❌",
        "CRITICAL": "💥",
    }

    def format(self, record):
        record.emoji = self.EMOJIS.get(record.levelname, "❓")
        return super().format(record)

def configure_logging():
    logging.basicConfig(level=SETTINGS["LOG_LEVEL"])
    handler = logging.StreamHandler()
    handler.setFormatter(
        EmojiFormatter("%(asctime)s %(name)s %(emoji)s [%(levelname)s] %(message)s")
    )
    logging.root.handlers = [handler]

    if SETTINGS["LOG_TO_FILE"]:
        file_handler = logging.FileHandler(SETTINGS["LOG_FILE_PATH"])
        file_handler.setFormatter(logging.Formatter("%(asctime)s %(name)s [%(levelname)s] %(message)s"))
        logging.root.addHandler(file_handler)

    logger = logging.getLogger(__name__)
    logger.debug("Logging configured.")
    if SETTINGS["DEMO_LOGS"]:
        logger.debug("Debug log")
        logger.info ("Info log")
        logger.warning("Warning log")
        logger.error("Error log")
        logger.critical("Critical log")

# configure as soon as the package is imported
configure_logging()