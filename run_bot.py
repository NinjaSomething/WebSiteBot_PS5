import logging
import yaml
from walmart_bot import MandalorianBot

STANDARD_LOG_FORMAT = "[{levelname}] {asctime}|{module}:{lineno} - {message}"
DATE_FORMAT = "%Y-%m-%dT%H:%M:%S"

logger = logging.getLogger(__name__)


if __name__ == "__main__":
    logging.basicConfig(format=STANDARD_LOG_FORMAT, level=logging.INFO, datefmt="%m-%d-%y %H:%M:%S", style="{")
    logger.setLevel(logging.DEBUG)

    with open("personal_info.yml") as f:
        personal_info = yaml.safe_load(f)

    bot = MandalorianBot(**personal_info)
    logger.info("FINISHED!")
    sys.exit(0)
