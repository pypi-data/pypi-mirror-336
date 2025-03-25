from pathlib import Path
import logging
import logging.handlers

CURRENT = Path(__file__).resolve().parent
log_file = CURRENT.parent.joinpath("soda-ahk.cursor.log")
# Create a handler and set format
handler = logging.handlers.RotatingFileHandler(
    log_file,
    mode="a",
    maxBytes=1024 * 1024 * 10,
    backupCount=5,
    encoding="utf8",
    delay=True,
    errors=None,
)
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
handler.setFormatter(formatter)
logger = logging.getLogger(__name__)
logger.addHandler(handler)
logger.setLevel(logging.INFO)