from ahk_cursor.api import GetProcessByName
from ahk_cursor.logger import logger


def check_running():
    ret = GetProcessByName("BGI.exe")
    if not ret:
        logger.info("BGI not running")
        return -1
    else:
        logger.info("BGI running")
        return ret
