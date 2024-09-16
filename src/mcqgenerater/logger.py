import logging
import os
from datetime import datetime

LOG_FILE = f"{datetime.now().strftime('%m_%d_%Y_%H_%M_%S')}.log"

log_file_path = os.path.join(os.getcwd(), "logs")
os.makedirs(log_file_path, exist_ok=True)  # create directory if not exist

LOG_FILE_PATH = os.path.join(log_file_path, LOG_FILE)

logging.basicConfig(
    filename=LOG_FILE_PATH,
    level=logging.INFO,
    format="[ %(asctime)s ] %(lineno)d %(name)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger(__name__)